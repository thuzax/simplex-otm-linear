
def install_package(package):
    import os
    text = "O pacote " + str(package) + " é necessário para a execução. " 
    text += "Deseja instalá-lo [S/n]? "
    answer = input(text)
    if (answer != "s" and answer != "S" and answer != ""):
        text = "O pacote " 
        text += str(package) 
        text += " é necessário para a execução. Finalizando."
        print(text)
        exit(0)
    print("Tentando instalar o pacote " + str(package))
    result = os.system("sudo apt install python-" + str(package))
    result = os.system("sudo apt install python3-" + str(package))
    if (result != 0):
        print("Não foi possível instalar o pacote " + str(package))
        print("Será necessário fazer a instalação manual.")
        print("Reexecute o programa após finalizar a instalação")
        exit(0)

def verify_package_installed(package):
    import importlib.util
    spec_result = importlib.util.find_spec(package)
    if (spec_result is None):
        return False
    return True