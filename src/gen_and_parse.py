import re
import sys


def read_file_content(path):
    with open(path, 'r')as fc:
        return fc.readlines()


def delete_comments(file_content):
    stripped_file_content = []
    for line in file_content:
        string_temp = re.sub(r'--.*', '', line).strip()  # Removing comments and newline characters
        string_temp = re.sub(r' +', ' ', string_temp)
        stripped_file_content.append(string_temp)
    stripped_file_content = [x for x in stripped_file_content if x != '']

    return stripped_file_content


def parse_libs(file_content):
    return [x for x in file_content if re.search(r'(library|use).*', x, re.IGNORECASE) is not None]


def parse_entity(file_content):
    for line in file_content:
        re_match = re.match(r'entity (.*) is', line, re.IGNORECASE)
        if re_match:
            module_name = re_match.group(1)
            break
    else:
        print('Did not find any module name.')
        sys.exit()

    string_content = '\n'.join(file_content)
    regex_pattern = rf'entity.*{module_name} is.*port *\( *(.*)( +)?\) *;.*end.*{module_name} *;'
    raw_portlist = (re.search(regex_pattern, string_content, re.DOTALL | re.MULTILINE | re.IGNORECASE).group(1)).split('\n')

    ports = {}

    for port in raw_portlist:
        if port == '':
            continue
        port_name, port_spec = port.split(':')
        port_name = port_name.strip()
        ports[port_name] = []

        if 'in' in port_spec or 'IN' in port_spec:
            spec = re.split('in', port_spec, flags=re.IGNORECASE)[-1]
            ports[port_name].append('in')
            ports[port_name].append(spec.strip())
        elif 'out' in port_spec or 'OUT' in port_spec:
            spec = re.split('out', port_spec, flags=re.IGNORECASE)[-1]
            ports[port_name].append('out')
            ports[port_name].append(spec.strip())
        elif 'inout' in port_spec or 'INOUT' in port_spec:
            spec = re.split('inout', port_spec, flags=re.IGNORECASE)[-1]
            ports[port_name].append('inout')
            ports[port_name].append(spec.strip())
        elif 'buffer' in port_spec or 'BUFFER' in port_spec:
            spec = re.split('buffer', port_spec, flags=re.IGNORECASE)[-1]
            ports[port_name].append('buffer')
            ports[port_name].append(spec.strip())
        elif 'linkage' in port_spec or 'LINKAGE' in port_spec:
            spec = re.split('linkage', port_spec, flags=re.IGNORECASE)[-1]
            ports[port_name].append('linkage')
            ports[port_name].append(spec.strip())

    return ports, module_name


def create_tb(libs, ports, module_name, output_path):
    tb_name = f'tb_{module_name}'

    portlist = ''
    for port_name, port_spec in ports.items():
        portlist += f'\t\t\t{port_name}\t:\t{port_spec[0]} {port_spec[1]}\n'
    portlist = portlist[:-1]

    tb_content = "-- Generated by Fintor Jozsef's script.\n\n"
    # ports
    tb_content += '\n'.join(libs) + '\n\n'
    tb_content += f'entity {tb_name} is\nend {tb_name};\n\n'
    tb_content += f'architecture tb of {tb_name} is\n'
    tb_content += f'\tcomponent {module_name}\n'
    tb_content += f'\t\tport (\n{portlist});\n\tend component;\n\n'

    # signals
    signals = ''
    for port_name, port_spec in ports.items():
        signals += f'\t signal {port_name}\t: {port_spec[1]}\n'
    signals = signals[:-1]
    tb_content += f'{signals};\n\n'

    tb_content += 'begin\n\n'
    tb_content += f'\tdut : {module_name}\n'
    tb_content += f'\tport map (\n'
    port_map = ''
    for port_name, port_spec in ports.items():
        port_map += f'\t\t\t{port_name}\t => {port_name},\n'
    port_map = port_map[:-2]  # removing ',\n'
    tb_content += f'{port_map});\n\n'
    tb_content += '\tstimuli : process\n\n'
    tb_content += '\tbegin\n'
    tb_content += '\t\t-- Write initialization here.\n\n\n'
    tb_content += '\t\t-- Write stimuli here.\n\n\n'
    tb_content += '\t\twait;\n'
    tb_content += '\tend process;\n\n'
    tb_content += 'end tb;'
    with open(output_path, 'w') as of:
        of.write(tb_content)


def get_stuff(filepath):
    vhdl_content = read_file_content(filepath)
    stripped_content = delete_comments(vhdl_content)
    libs = parse_libs(stripped_content)
    ports, module_name = parse_entity(stripped_content)
    return ports, module_name, libs


def write_const_to_file(port_and_package_dict, output_path, use_onboard_clock):
    const_content = "## Generated by Fintor Jozsef's script.\n\n"

    if 'Clock' in port_and_package_dict.keys():
        const_content += '## Clock signal\n'
        const_content += f'set_property PACKAGE_PIN E3 [get_ports {{{port_and_package_dict["Clock"]}}}]\n'
        const_content += f'\tset_property IOSTANDARD LVCMOS33 [get_ports {{{port_and_package_dict["Clock"]}}}]\n'
        if use_onboard_clock:
            const_content += f'\tcreate_clock -add -name sys_clk_pin -period 10.00 -waveform {{0 5}} [get_ports {{{port_and_package_dict["Clock"]}}}];\n\n'
        else:
            const_content += '\n'
        del port_and_package_dict['Clock']

    for port_name, package_pin in port_and_package_dict.items():
        port_name = '{' + port_name + '}'
        const_content += f'set_property PACKAGE_PIN {package_pin} [get_ports {port_name}]\n'
        const_content += f'\t set_property IOSTANDARD LVCMOS33 [get_ports {port_name}]\n\n'

    with open(output_path, 'w') as of:
        of.write(const_content)


def generate_tb(filepath, output_path):
    ports, module_name, libs = get_stuff(filepath)
    create_tb(libs, ports, module_name, output_path)
