import os
import win32evtlog
import datetime
import xml.etree.ElementTree as ET
import tkinter as tk
from tkinter import ttk, scrolledtext
import paramiko

def load_ssh_key(key_file_path):
    try:
        key = paramiko.RSAKey.from_private_key_file(key_file_path)
        return key
    except Exception as e:
        print(f"Error loading SSH key: {e}")
        return None

def get_remote_event_logs(device, log_name, ssh_key):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(device, pkey=ssh_key)
        command = f'wevtutil qe {log_name} /f:xml'
        stdin, stdout, stderr = ssh.exec_command(command)
        logs = []
        for line in stdout:
            logs.append(line.strip())
        ssh.close()
        return logs
    except Exception as e:
        print(f"Error querying {device} event log: {e}")
        return []

ssh_key_path = r'E:\final year p\keys' # Update this path to your SSH key file
ssh_key = load_ssh_key(ssh_key_path)
if not ssh_key:
    print("Failed to load SSH key. Exiting.")
    exit(1)

def get_all_event_logs(log_name, devices):
    try:
        logs = []
        for device in devices:
            device_logs = get_remote_event_logs(device, log_name, ssh_key) # Pass ssh_key here
            logs.extend(device_logs)
        return logs
    except Exception as e:
        print(f"Error querying {log_name} event log: {e}")
        return []

def write_logs_to_xml(logs, file_path):
    try:
        root = ET.Element("EventLogs")
        for log in logs:
            log_elem = ET.SubElement(root, "Log")
            ET.SubElement(log_elem, "EventID").text = str(log['EventID'])
            ET.SubElement(log_elem, "TimeGenerated").text = log['TimeGenerated']
            ET.SubElement(log_elem, "EventType").text = str(log['EventType'])
            ET.SubElement(log_elem, "ComputerName").text = log['ComputerName']
            ET.SubElement(log_elem, "UserName").text = log['UserName']
            ET.SubElement(log_elem, "Category").text = str(log['Category'])
            ET.SubElement(log_elem, "Message").text = log['Message']

        tree = ET.ElementTree(root)
        tree.write(file_path, encoding='utf-8', xml_declaration=True)
        print(f"Logs have been written to: {file_path}")
    except Exception as e:
        print(f"Error writing logs to XML file: {e}")

def transfer_logs_to_host(host_device, ssh_key, xml_file_paths):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host_device, pkey=ssh_key)
        for xml_file_path in xml_file_paths:
            sftp = ssh.open_sftp()
            sftp.put(xml_file_path, f"{os.path.basename(xml_file_path)}")
            sftp.close()
        ssh.close()
        print(f"Logs transferred to {host_device}")
    except Exception as e:
        print(f"Error transferring logs to {host_device}: {e}")

# Define the list of devices and the log name
devices = ['192.168.151.138', '192.168.151.203', '192.168.151.42'] # Include the host device IP here
log_name = 'Security' # Change to 'Security' to retrieve security logs

# Retrieve the logs from all devices and write them to XML files
xml_file_paths = []
for device in devices:
    logs = get_all_event_logs(log_name, [device])
    if logs:
        xml_file_path = f"{log_name}_{device}.xml"
        write_logs_to_xml(logs, xml_file_path)
        xml_file_paths.append(xml_file_path)

# Transfer logs to the host device
host_device = '192.168.151.1' # Update this to the host device IP
transfer_logs_to_host(host_device, ssh_key, xml_file_paths)

# The rest of your script remains the same

def show_details(event_id, xml_file_path, text_widget):
    try:
        tree = ET.parse(xml_file_path)
        root = tree.getroot()

        text_widget.delete(1.0, tk.END)  # Clear existing text

        # Retrieve and display details only for the selected Event ID
        for log in root.findall('Log'):
            if int(log.find('EventID').text) == event_id:
                text_widget.insert(tk.END, f"Event ID: {event_id}\n")
                text_widget.insert(tk.END, f"Details for Event ID {event_id}:\n")
                text_widget.insert(tk.END, "-" * 40 + "\n")
                text_widget.insert(tk.END, f"Time Generated: {log.find('TimeGenerated').text}\n")
                text_widget.insert(tk.END, f"Event Type: {log.find('EventType').text}\n")
                text_widget.insert(tk.END, f"Computer Name: {log.find('ComputerName').text}\n")
                text_widget.insert(tk.END, f"User Name: {log.find('UserName').text}\n")
                text_widget.insert(tk.END, f"Category: {log.find('Category').text}\n")
                text_widget.insert(tk.END, f"Message: {log.find('Message').text}\n\n")
                break

    except Exception as e:
        print(f"Error displaying details for Event ID {event_id}: {e}")

def display_logs_as_table(xml_file_paths, treeview, text_widget):
    try:
        for xml_file_path in xml_file_paths:
            tree = ET.parse(xml_file_path)
            root = tree.getroot()

            # Clear existing items in the Treeview
            treeview.delete(*treeview.get_children())

            for log in root.findall('Log'):
                event_id = int(log.find('EventID').text)
                time_generated = log.find('TimeGenerated').text
                event_type = int(log.find('EventType').text)
                computer_name = log.find('ComputerName').text
                user_name = log.find('UserName').text
                category = int(log.find('Category').text)
                message = log.find('Message').text

                # Insert the row with Event ID as tag to visually separate events
                treeview.insert('', 'end',values=(event_id, time_generated, event_type, computer_name, user_name, category, message),
                                 tags=(f"Event{event_id}",))

                # Store the complete log details for each Event ID
                text_widget.insert(tk.END, f"Event ID: {event_id}\nTime Generated: {time_generated}\nEvent Type: {event_type}\n"
                                           f"Computer Name: {computer_name}\nUser Name: {user_name}\nCategory: {category}\n"
                                           f"Message: {message}\n\n")
                text_widget.tag_add(f"Event{event_id}", text_widget.index(tk.END) + "-4l", text_widget.index(tk.END))

    except Exception as e:
        print(f"Error displaying logs as a table: {e}")

def on_select(event):
    try:
        selected_item = treeview.focus()
        event_id = int(treeview.item(selected_item)['values'][0])
        xml_file_path = xml_file_paths[treeview.index(selected_item)]
        show_details(event_id, xml_file_path, text_widget)
    except Exception as e:
        print(f"Error displaying details for selected event: {e}")

# Define the list of devices and the log name
devices = ['192.168.151.138', '192.168.151.203', '192.168.151.42']
log_name = 'System'

# Retrieve the logs from all devices and write them to XML files
xml_file_paths = []
for device in devices:
    logs = get_all_event_logs(log_name, [device])
    if logs:
        xml_file_path = f"{log_name}_{device}.xml"
        write_logs_to_xml(logs, xml_file_path)
        xml_file_paths.append(xml_file_path)

# Create the GUI
root = tk.Tk()
root.title("Log Analyzer")

# Create the Treeview and Text widgets
treeview = ttk.Treeview(root, columns=('EventID', 'TimeGenerated', 'EventType', 'ComputerName', 'UserName', 'Category', 'Message'))
treeview.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

treeview.heading('#0', text='Event ID')
treeview.heading('#1', text='Time Generated')
treeview.heading('#2', text='Event Type')
treeview.heading('#3', text='Computer Name')
treeview.heading('#4', text='User Name')
treeview.heading('#5', text='Category')
treeview.heading('#6', text='Message')

treeview.column('#0', width=50, minwidth=50, stretch=True)
treeview.column('#1', width=150, minwidth=150, stretch=True)
treeview.column('#2', width=50, minwidth=50, stretch=True)
treeview.column('#3', width=150, minwidth=150, stretch=True)
treeview.column('#4', width=150, minwidth=150, stretch=True)
treeview.column('#5', width=50, minwidth=50, stretch=True)
treeview.column('#6', width=500, minwidth=500, stretch=True)

treeview.bind('<ButtonRelease-1>', on_select)

text_widget = scrolledtext.ScrolledText(root, wrap=tk.NONE, width=80, height=20)
text_widget.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

# Display the logs as a table
display_logs_as_table(xml_file_paths, treeview, text_widget)

root.mainloop()
