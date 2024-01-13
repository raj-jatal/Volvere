import platform
import psutil
import speedtest 
import wmi
import ctypes
from screeninfo import get_monitors
import winreg

def get_installed_software():
    software_list = []
    uninstall_key = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"
    
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, uninstall_key) as key:
            for i in range(winreg.QueryInfoKey(key)[0]):
                subkey_name = winreg.EnumKey(key, i)
                subkey_path = uninstall_key + "\\" + subkey_name
                
                try:
                    with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, subkey_path) as subkey:
                        display_name, _ = winreg.QueryValueEx(subkey, "DisplayName")
                        if display_name:
                            software_list.append(display_name)
                except FileNotFoundError:
                    pass
    except Exception as e:
        print(f"Error: {e}")
    
    return software_list


def get_internet_speed():
    print("i am inside the funtion")
    st = speedtest.Speedtest()
    download_speed = st.download() / 1024 / 1024
    upload_speed = st.upload() / 1024 / 1024
    return download_speed, upload_speed

def get_screen_resolution():
    monitors = get_monitors()
    resolutions = [(monitor.width, monitor.height) for monitor in monitors]
    return resolutions

def get_cpu_info():
    cpu_info = {}
    cpu_info['model'] = platform.processor()
    cpu_info['cores'] = psutil.cpu_count(logical=False)
    cpu_info['threads'] = psutil.cpu_count(logical=True)
    return cpu_info

def get_gpu_info():
    try:
        w = wmi.WMI()
        gpu_info = w.Win32_VideoController()[0].Caption
    except Exception:
        gpu_info = "N/A"
    return gpu_info

def get_ram_size():
    ram_info = psutil.virtual_memory()
    ram_size_gb = ram_info.total / (1024 ** 3)
    return ram_size_gb

def get_screen_size():
    if platform.system() == "Windows":
        return get_windows_screen_size()
    else:
        return "Not implemented for this platform"

def get_windows_screen_size():
    try:

        user32 = ctypes.windll.user32
        width = user32.GetSystemMetrics(0)
        height = user32.GetSystemMetrics(1)
        #standard DPI value of 157
        diagonal_size = ((width / 157) ** 2 + (height /157) ** 2) ** 0.5
        return diagonal_size
    except Exception as e:
        return f"Error fetching screen size: {e}"

def get_network_info():
    network_info = {}
    try:
        for interface, addrs in psutil.net_if_addrs().items():
            for addr in addrs:
                if addr.family == psutil.AF_LINK: 
                    network_info['mac_address'] = addr.address
                    break
            if 'mac_address' in network_info:
                break
    except Exception as e:
        network_info['mac_address'] = "N/A"
    try:
        network_info['public_ip'] = psutil.net_if_addrs()['Wi-Fi'][0].address
    except Exception as e:
        network_info['public_ip'] = "N/A"
    return network_info['mac_address'], network_info['public_ip']

def get_windows_version():
    return platform.version()

if __name__ == "__main__":
    print("\nPrinting the All Installed software’s list :: ")

    installed_software = get_installed_software()
    if installed_software:
        print("Installed Software:")
        for software in installed_software:
            print("- " + software)
    else:
        print("No software information available.")
    # print("Printing the Internet Speed :: ")
    # internet_speed = get_internet_speed()
    # try:
    #     internet_speed = get_internet_speed()
    #     print("Internet Speed (Download, Upload): ", internet_speed)
    # except Exception as e:
    #     print(f"Error fetching internet speed: {e}") 
         
    print("\nPrinting the Screen Resolution :: ")           
    screen_resolution = get_screen_resolution()
    print("Screen Resolution: ", screen_resolution)

    print("\nPrinting the CPU Information :: ")
    cpu_info = get_cpu_info()
    print("CPU Info: ", cpu_info)

    print("\nPrinting the GPU Information :: ")
    gpu_info = get_gpu_info()
    print("GPU Info: ", gpu_info)

    print("\nPrinting the Ram Size :: ")
    ram_size = get_ram_size()
    print("RAM Size: ", ram_size, "GB")

    print("\nPrinting the Screen Size :: ")
    screen_size = get_screen_size()
    print("Screen Size (in inches): ", screen_size)

    print("\nPrinting the Windows Version :: ")
    windows_version = get_windows_version()
    print("Windows Version: ", windows_version)

    print("\nPrinting the MAC Address and IP Address :: ")
    try:
        mac_address, public_ip = get_network_info()
        print("MAC Address: ", mac_address)
        print("Public IP Address: ", public_ip)
    except Exception as e:
        print(f"Error fetching network information: {e}")




    

    
