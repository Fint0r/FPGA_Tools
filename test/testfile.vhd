----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date: 03.05.2020 18:07:11
-- Design Name:
-- Module Name: alu - Behavioral
-- Project Name:
-- Target Devices:
-- Tool Versions:
-- Description:
--
-- Dependencies:
--
-- Revision:
-- Revision 0.01 - File Created
-- Additional Comments:
--
----------------------------------------------------------------------------------


library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

-- Uncomment the following library declaration if using
-- arithmetic functions with Signed or Unsigned values
--use IEEE.NUMERIC_STD.ALL;

-- Uncomment the following library declaration if instantiating
-- any Xilinx leaf cells in this code.
--library UNISIM;
--use UNISIM.VComponents.all;

entity alu is
    Port (


    addr : in STD_LOGIC_VECTOR (3 downto 0);

           a_reg : in STD_LOGIC_VECTOR (7 downto 0);--lofasz
           b_reg : in STD_LOGIC_VECTOR (7 downto 0);
           c_out_alu : out STD_LOGIC;
           alu_out : out STD_LOGIC_VECTOR (7 downto 0)


           );
end alu;

architecture Behavioral of alu is
    component add_sub
        Port (  A : in STD_LOGIC_VECTOR (7 downto 0);
                B : in STD_LOGIC_VECTOR (7 downto 0);
                C_in : in STD_LOGIC;
                C_out : out STD_LOGIC;
                S : out STD_LOGIC_VECTOR (7 downto 0));
    end component;

    component mux
        Port (  add_sub_input : in STD_LOGIC_VECTOR (7 downto 0);
                and_input : in STD_LOGIC_VECTOR (7 downto 0);
                or_input : in STD_LOGIC_VECTOR (7 downto 0);
                lefts_input : in STD_LOGIC_VECTOR (7 downto 0);
                rights_input : in STD_LOGIC_VECTOR (7 downto 0);
                addr_input : in STD_LOGIC_VECTOR (3 downto 0);
                mux_output : out STD_LOGIC_VECTOR (7 downto 0));
      end component;

    component and_func
        Port (  input_a_and : in STD_LOGIC_VECTOR (7 downto 0);
                input_b_and : in STD_LOGIC_VECTOR (7 downto 0);
                output_a_and : out STD_LOGIC_VECTOR (7 downto 0));
    end component;

    component or_func
        Port (  input_a_or : in STD_LOGIC_VECTOR (7 downto 0);
                input_b_or : in STD_LOGIC_VECTOR (7 downto 0);
                output_a_or : out STD_LOGIC_VECTOR (7 downto 0));
    end component;

    component xor_func
        Port (  input_b_xor : in STD_LOGIC_VECTOR (7 downto 0);
                select_xor : in STD_LOGIC;
                output_b_xor : out STD_LOGIC_VECTOR (7 downto 0));
    end component;


    signal xored_b : STD_LOGIC_VECTOR (7 downto 0);
    signal adder_output : STD_LOGIC_VECTOR (7 downto 0);
    signal anded : STD_LOGIC_VECTOR (7 downto 0);
    signal ored : STD_LOGIC_VECTOR (7 downto 0);
    signal left_shifted : STD_LOGIC_VECTOR (7 downto 0);
    signal right_shifted : STD_LOGIC_VECTOR (7 downto 0);

    signal c_out_correction : STD_LOGIC;
begin
     left_shifted(0) <= '0';
     LEFT_SHIFTING: for I in 1 to 7 generate
        left_shifted(I) <= a_reg(I-1);
     end generate LEFT_SHIFTING;

     right_shifted(7) <= '0';
      RIGHT_SHIFTING: for I in 0 to 6 generate
        right_shifted(I) <= a_reg(I+1);
     end generate RIGHT_SHIFTING;

     c_out_alu <= (((addr(0) and (not addr(1)) and (not addr(2))) and c_out_correction) and (not addr(3)));       -- only turn on if proper operation is requested (addition)
     MAPPING_ADDER: add_sub port map (a_reg, xored_b, addr(3), c_out_correction, adder_output);
     MAPPING_MUX: mux port map (adder_output, anded, ored, left_shifted, right_shifted, addr, alu_out);

     MAPPING_AND_FUNC:  and_func port map (a_reg, xored_b, anded);
     MAPPING_OR_FUNC:   or_func port map (a_reg, xored_b, ored);
     MAPPING_XOR_FUNC:  xor_func port map (b_reg, addr(3), xored_b);
end Behavioral;
