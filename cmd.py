import click
import subprocess
import os
import pyshark
from test import test 
@click.command()
@click.option('--container_id', prompt="Please enter the container ID", help='The container ID.')

def capture(container_id):
    
    # get the container veth
    cmd_veth = "sh veth.sh " + container_id 
    result_veth = os.popen(cmd_veth)
    container_veth = result_veth.read()
    result_veth.close()

    pcap_name = "packet_pcap.pcap" 
    pcap_path = "/home/uscc/Ncsis_Docker_IDS/pcap/ "
    cve_path = "/home/uscc/Ncsis_Docker_IDS/csv/ "
    cvefile_path = "/home/uscc/Ncsis_Docker_IDS/csv/packet_pcap.pcap_Flow.csv"

    safe_allflow = [] 
    weak_alldangerflow = [] 
    strong_alldangerflow = []
    
#     while True:
#         # capture the packet from the container veth       
#         capture = pyshark.LiveCapture(output_file="/home/uscc/Ncsis_Docker_IDS/pcap/packet_pcap.pcap" , interface=container_veth)
#         capture.sniff(packet_count=100)
        
#         # analysis the packet
#         os.chdir("/home/uscc/Ncsis_Docker_IDS/CICFlowMeter-4.0/bin/")
#         cmd_analysis = "sh cfm " + pcap_path + cve_path
#         os.system(cmd_analysis)

#         # analysis the flow
#         os.chdir("/home/uscc/Ncsis_Docker_IDS")
#         safe_flow, weak_dangerflow, strong_dangerflow=test(cvefile_path)
#         safe_allflow.append(safe_flow)
#         weak_alldangerflow.append(weak_dangerflow)
#         strong_alldangerflow.append(strong_dangerflow)

        # analysis the packet
    os.chdir("/home/uscc/Ncsis_Docker_IDS/CICFlowMeter-4.0/bin/")
    cmd_analysis = "sh cfm " + "/home/uscc/Ncsis_Docker_IDS/analysis_pcap/ " + cve_path
    os.system(cmd_analysis)




        

 
if __name__ == '__main__':
    capture()
