import first_table
import second_table
import outro

first_table_var = first_table.first_table(
    "15888", "05/08/12", "50000", "20000", "99999")
second_table_var = second_table.second_table(
    "tiptop", "toptip", "05/05/12", "15:12")
outro_var = outro.outro()

a = second_table_var + first_table_var + outro_var


with open('C:/Users/guetec/OneDrive - CSB/Documents/projets/BCI_ON_US/bci_on_us/bin/my_data.html', "w") as file:
    file.write(a)
