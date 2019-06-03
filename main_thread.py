import click
import subprocess
import os
import pyshark
import time
import threading
import pandas as pd

from test import test 

# set the path
pcap_path = "/home/uscc/Ncsis_Docker_IDS/pcap/"
alypcap_path = "/home/uscc/Ncsis_Docker_IDS/analysis_pcap/"
cve_path = "/home/uscc/Ncsis_Docker_IDS/csv/"
cvefile_path = "/home/uscc/Ncsis_Docker_IDS/csv/packet_pcap.pcap_Flow.csv"
cicflowmeter_path = "/home/uscc/Ncsis_Docker_IDS/CICFlowMeter-4.0/bin/"

# set the result list
safe_allflow = [] 
weak_alldangerflow = [] 
strong_alldangerflow = []

container_id = "ea6fe2c9e877"

def flow_analysis():
    print("啟動分析流量")

    while True:
        print("開始分析封包")

        # capture the pcap file name from pcap Folder    
        pcap_files = os.listdir(pcap_path)
        if len(pcap_files) == 0:
            time.sleep(100)
        else:
            for name in pcap_files:
                full_pcap_name = os.path.join(pcap_path, name)
                cmd_mv = "mv " + full_pcap_name + " " + alypcap_path
                cmd_analysis = "sh cfm " + alypcap_path + " "+ cve_path
                try :
                    # move the pcap file from pcap folder to analysis_pcap folder 
                    os.system(cmd_mv)
                    # analysis the packet with CICFlowmeter
                    os.chdir(cicflowmeter_path)
                    os.system(cmd_analysis)
                except :
                    pass

                # capture the pcap file name from analysis_pcap folder 
                alypcap_files = os.listdir(alypcap_path)
                for name in alypcap_files:
                    full_alypcap_name = os.path.join(alypcap_path, name)
                    cmd_rm = "rm " + full_alypcap_name
                    try :
                        # delete the pcap file from analysis_pcap 
                        os.system(cmd_rm)
                    except:
                        pass

                # concat the analysis cve file
                cvename = []
                cve_files = os.listdir(cve_path)
                for name in cve_files:
                    full_cve_name = os.path.join(cve_path, name)
                    cvename.append(full_cve_name) 
                for i in range(len(cvename)):
                    try: 
                        os.chdir("/home/uscc/Ncsis_Docker_IDS")
                    except:
                        pass
                    # analysis the flow by deep learning model
                    safe_flow, weak_dangerflow, strong_dangerflow = test(cvename[i])
                    safe_allflow.append(safe_flow)
                    weak_alldangerflow.append(weak_dangerflow)
                    strong_alldangerflow.append(strong_dangerflow)
                    # print(safe_allflow)
                    
                    try:
                        # delete the csv file from csv folder 
                        os.system("rm " + cvename[i])
                    except:
                        pass

                print("結束此輪分析封包")
                print("繼續下輪封包分析")

    print("關閉分析流量")

def capture_packet():
    print("啟動抓取封包")
    while True:
        # get the container veth
        try:
            cmd_veth = "sh veth.sh " + container_id 
            result_veth = os.popen(cmd_veth)
            container_veth = result_veth.read()
            result_veth.close()
        except IOError as e:
            print("Error: %s" % e.strerror)

        print("抓取封包")
        # get the current time
        time_stamp = int(time.time())
        time_stamp = int(time_stamp* (10 ** (10-len(str(time_stamp)))))
        time_stamp = str(time_stamp)

        # set the pcap name with current time 
        pcap_name = "/home/uscc/Ncsis_Docker_IDS/pcap/" + time_stamp + ".pcap"

        # use pyshark to capture network packet
        capture = pyshark.LiveCapture(output_file=pcap_name , interface=container_veth)
        capture.sniff(packet_count=50)
    
    print("關閉抓取封包")

def main():
    thread_analysis = threading.Thread(target=flow_analysis, name='T1')
    thread_analysis.start()

    thread_capture = threading.Thread(target=capture_packet, name='T2')
    thread_capture.start()

if __name__ == "__main__":
    main()