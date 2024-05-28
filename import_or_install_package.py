import pip
import importlib.util

def install_package(package):
    text = "O pacote numpy é necessário para a execução. " 
    text += "Deseja instalá-lo [S/n]? "
    answer = input(text)
    print(answer == "S")
    if (answer != "s" and answer != "S" and answer != ""):
        print("Numpy é necessário para a execução. Finalizando.")
        exit(0)
    pip.main(['install', package])

def verify_package_installed(package):
    spec_result = importlib.util.find_spec(package)
    if (spec_result is None):
        return False
    return True