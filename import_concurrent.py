#!/usr/bin/python

import concurrent.futures
import subprocess

def run_command(runID):
    command = f'{EnaBT_path} -f {file_type} {runID} -d {path}'
    subprocess.run(command, check=True, shell=True, stdout=1, stderr=2)

EnaBT_path = "~/tools/enaBrowserTools-1.1.0/python3//enaDataGet"
file_type = "fastq"
path = "/root/sara/MADAME/Downloads/prova_down/PRJNA780434/PRJNA780434_fastq_files"
runIDs = ["SRR16947000", "SRR16946901"]  # Lista di runID da processare

with concurrent.futures.ThreadPoolExecutor() as executor:
    executor.map(run_command, runIDs)













# EnaBT_path = "/root/tools/enaBrowserTools-1.1.0/python3"
# file_type = "fastq"
# path = "/root/sara/MADAME/Downloads/prova_down/PRJNA780434/PRJNA780434_fastq_files"




# # Create a ThreadPoolExecutor with a maximum number of worker threads
# executor = ThreadPoolExecutor(max_workers=100)
# # Use a list to store the download tasks
# download_tasks = []
# # Submit the download tasks
# for file_url in runIDs:
#     download_task = executor.submit(download_file, file_url)
#     download_tasks.append(download_task)
# # Process the completed tasks
# for completed_task in as_completed(download_tasks):
#     result = completed_task.result()
#     # Handle the downloaded file
#     process_file(result)





# def execute_command(runID):
#     # Simulazione di download
#     # Qui puoi creare un file locale con dati di test anziché scaricare effettivamente da Internet

#     # Esecuzione del comando
#     command = f'{EnaBT_path} -f {file_type} {runID} -d {path}'
#     result = subprocess.run(command, check=True, shell=True, stdout=1, stderr=2)
#     return result.stdout, result.stderr

# def main():
#     runIDs = ["SRR16946900"] #SRR16947000  # Lista di esempio di runID

#     with concurrent.futures.ThreadPoolExecutor() as executor:
#         # Mappa la funzione di esecuzione sui runID con i risultati come argomenti
#         results = executor.map(execute_command, runIDs)

#     # Stampa i risultati
#     for result in results:
#         stdout, stderr = result
#         print(f"stdout: {stdout.decode()}")
#         print(f"stderr: {stderr.decode()}")

# if __name__ == "__main__":
#     main()



# main()