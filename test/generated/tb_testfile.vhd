--Generated by Fintor Jozsef's script.

library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity tb_alu is
end tb_alu;

architecture tb of tb_alu is
	component alu
		port (
			addr	:	in STD_LOGIC_VECTOR (3 downto 0);
			a_reg	:	in STD_LOGIC_VECTOR (7 downto 0);
			b_reg	:	in STD_LOGIC_VECTOR (7 downto 0);
			c_out_alu	:	out STD_LOGIC;
			alu_out	:	out STD_LOGIC_VECTOR (7 downto 0));
	end component;

	 signal addr	: STD_LOGIC_VECTOR (3 downto 0);
	 signal a_reg	: STD_LOGIC_VECTOR (7 downto 0);
	 signal b_reg	: STD_LOGIC_VECTOR (7 downto 0);
	 signal c_out_alu	: STD_LOGIC;
	 signal alu_out	: STD_LOGIC_VECTOR (7 downto 0);

begin

	dut : alu
	port map (
			addr	 => addr,
			a_reg	 => a_reg,
			b_reg	 => b_reg,
			c_out_alu	 => c_out_alu,
			alu_out	 => alu_out);

	stimuli : process

	begin
		-- Write initialization here.


		-- Write stimuli here.


		wait;
	end process;

end tb;