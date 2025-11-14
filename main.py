import sys
from lexer import lexer
from grammar import parse_input, variables

def main(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            data = file.read()
        
        parse_input(data)

        print("\nVariáveis finais:")
        for var, value in variables.items():
            print(f"{var} = {value}")

    except FileNotFoundError:
        print(f"Arquivo {filename} não encontrado.")
    except Exception as e:
        print(f"Ocorreu um erro: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python main.py <arquivo_de_entrada>")
    else:
        main(sys.argv[1])