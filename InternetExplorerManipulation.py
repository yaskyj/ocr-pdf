# Improvements
from time import time as time2
import time, win32ui, win32gui, win32com, pythoncom, win32con, csv, os, winsound, sys
from win32com.client import Dispatch
import pyautogui

def PushButton(handle, label):
    if win32gui.GetWindowText(handle) == label:
        win32gui.SendMessage(handle, win32con.BM_CLICK, None, None)
        return True

def enum_callback(hwnd, results):
    winlist.append((hwnd, win32gui.GetWindowText(hwnd)))

def make_sound(freq, dur):
    winsound.Beep(freq, dur)
    winsound.Beep(freq, dur)
    winsound.Beep(freq, dur)

def make_error_email(image_number):
    olMailItem = 0x0
    obj = Dispatch("Outlook.Application")
    newMail = obj.CreateItem(olMailItem)
    newMail.Subject = "Error On Image " + image_number
    newMail.Body = "There was an error during download for image " + image_number
    newMail.To = "jroge12@entergy.com"
    newMail.Send()

def make_completion_email():
    olMailItem = 0x0
    obj = Dispatch("Outlook.Application")
    newMail = obj.CreateItem(olMailItem)
    newMail.Subject = "Download Batch Complete"
    newMail.Body = "Current batch downloads are complete."
    newMail.To = "jroge12@entergy.com"
    newMail.Send()

ie = Dispatch("InternetExplorer.Application")
ie.Visible = 1
# images = ['42679232', '42407359', '42531238', '42520534', '42520542']
images = ['41026939', '41026944'] # , '41026954', '41026968', '41027270', '41027578', '41027658', '41027661', '41027722', '41027725', '41027817', '41028388', '41030314', '41032479', '41032490', '41032710', '41032853', '41033359', '41033733', '41034365', '41034373', '41034384', '41034433', '41034436', '41034483', '41034487', '41034678', '41034863', '41034880', '41034970', '41034993', '41035999', '41037086', '41037259', '41037261', '41037849', '41038016', '41038035', '41038074', '41038636', '41038796', '41038821', '41038832', '41038834', '41038852', '41038988', '41039002', '41039004', '41039021', '41039024', '41039080', '41040602', '41044418', '41044428', '41044431', '41044435', '41044442', '41044462', '41044472', '41044475', '41044478', '41044488', '41044625', '41045094', '41045165', '41045187', '41045207', '41046229', '41046231', '41046235', '41046309', '41046311', '41046315', '41046329', '41046361', '41046366', '41046379', '41046381', '41046383', '41046385', '41046387', '41046389', '41046399', '41046401', '41046403', '41046461', '41047594', '41047680', '41047682', '41047720', '41047722', '41048591', '41048596', '41049141', '41049238', '41049274', '41049335', '41050887', '41050890', '41050894', '41051497', '41051499', '41051502', '41051505', '41051541', '41051543', '41051545', '41051571', '41054698', '41054701', '41054704', '41054707', '41054723', '41062127', '41062310', '41062570', '41062590', '41062593', '41062604', '41062625', '41063352', '41063382', '41063394', '41063417', '41063430', '41063436', '41063459', '41063494', '41063557', '41063565', '41063595', '41063887', '41064225', '41064264', '41064299', '41064421', '41064980', '41065127', '41065349', '41065385', '41065482', '41065489', '41065493', '41066182', '41066202', '41066270', '41066276', '41066305', '41066352', '41066379', '41066382', '41066396', '41066399', '41067347', '41067355', '41067409', '41067412', '41067415', '41067428', '41067436', '41067442', '41067444', '41067460', '41067463', '41067467', '41069515', '41069523', '41069526', '41069886', '41070306', '41071946', '41071949', '41072037', '41072039', '41072566', '41073336', '41073543', '41073554', '41073645', '41074497', '41074526', '41074528', '41074533', '41074658', '41077675', '41078038', '41078599', '41078698', '41079193', '41079556', '41079820', '41080216', '41080227', '41081164', '41081218', '41081221', '41081230', '41081236', '41081272', '41083232', '41083308', '41083310', '41083327', '41083341', '41084310', '41084314', '41084332', '41084337', '41084340', '41084416', '41084419', '41084424', '41084474', '41084522', '41084720', '41084746', '41084868', '41085361', '41085389', '41085465', '41085492', '41085495', '41085576', '41085581', '41085583', '41085698', '41085701', '41085705', '41085728', '41085731', '41085735', '41085738', '41085744', '41085748', '41085838', '41086207', '41086708', '41086881', '41086885', '41086889', '41086930', '41087190', '41087198', '41089057', '41089154', '41089961', '41089994', '41090016', '41090214', '41090434', '41090709', '41090720', '41090742', '41091204', '41091402', '41091677', '41091941', '41091963', '41092524', '41092997', '41093460', '41093465', '41094570', '41094711', '41094720', '41094722', '41094726', '41094738', '41094740', '41094743', '41094807', '41094810', '41094813', '41094816', '41095628', '41095649', '41095664', '41095759', '41095811', '41095824', '41098808', '41100172', '41100228', '41100360', '41100364', '41100366', '41100414', '41100595', '41100598', '41100601', '41103234', '41103245', '41103454', '41103487', '41103641', '41104180', '41104191', '41104609', '41104664', '41106087', '41106089', '41107035', '41112132', '41112638', '41112640', '41112642', '41112645', '41112936', '41112995', '41113028', '41113366', '41113398', '41113406', '41113457', '41113560', '41113637', '41113669', '41113758', '41113933', '41114098', '41114315', '41114372', '41114429', '41114465', '41115249', '41115318', '41115397', '41115411', '41115441', '41115555', '41115687', '41115817', '41115820', '41115847', '41115918', '41116058', '41116181', '41116199', '41116215', '41116517', '41116633', '41116720', '41116879', '41117143', '41117184', '41117269', '41117319', '41117329', '41117344', '41117964', '41117971', '41117991', '41117993', '41118248', '41118261', '41118397', '41118539', '41118772', '41123596', '41123601', '41123635', '41123805', '41123822', '41123865', '41123921', '41123941', '41123973', '41124048', '41124129', '41124181', '41124296', '41124699', '41125326', '41126382', '41126454', '41126546', '41126550', '41127069', '41127119', '41127186', '41127214', '41127232', '41127327', '41133315', '41133320', '41133815', '41134333', '41134381', '41135555', '41135872', '41135891', '41135900', '41135961', '41135967', '41135973', '41135990', '41136092', '41136100', '41136114', '41136119', '41136282', '41136287', '41136293', '41136297', '41137065', '41137078', '41137084', '41137107', '41137426', '41137916', '41138580', '41139021', '41139072', '41139155', '41139256', '41140315', '41140404', '41148554', '41148599', '41148623', '41148645', '41148647', '41148714', '41148745', '41148751', '41148753', '41148755', '41148757', '41148790', '41148792', '41148794', '41148796', '41148798', '41148821', '41148825', '41148827', '41148829', '41148852', '41148857', '41148909', '41148911', '41149434', '41149489', '41149539', '41149542', '41149557', '41149559', '41149604', '41149626', '41149628', '41149955', '41150048', '41150057', '41150070', '41150318', '41150328', '41150331', '41151284', '41151525', '41151836', '41151840', '41152005', '41152014', '41152040', '41152044', '41152287', '41152292', '41152359', '41152428', '41152432', '41152455', '41152458', '41152484', '41152545', '41152585', '41153486', '41153488', '41153532', '41153548', '41154125', '41154134', '41154145', '41154155', '41154180', '41154200', '41154209', '41154218', '41154227', '41154236', '41154345', '41154835', '41154837', '41154846'

for image_number in images:
    try:
        toplist = []
        winlist = []

        ie.Navigate('http://caw.entergy.com/IDMWS/cawFNDocView2.asp?docID=' + image_number)
        time.sleep(3)  # wait until IE is started

        win32gui.EnumWindows(enum_callback, toplist)
        page = [(hwnd, title) for hwnd, title in winlist if "Internet Explorer" in title]
        page = page[0]
        win32gui.SetForegroundWindow(page[0])

        wnd = win32ui.GetForegroundWindow()
        time.sleep(1)        
        # win32gui.EnumChildWindows(wnd.GetSafeHwnd(), PushButton, "&Open")
        pyautogui.press('enter')
        time.sleep(3)

        wnd = win32ui.GetForegroundWindow()
        win32gui.ShowWindow(wnd.GetSafeHwnd(), win32con.SW_MAXIMIZE)
        time.sleep(2)

        screenWidth, screenHeight = pyautogui.size()
        currentMouseX, currentMouseY = pyautogui.position()
        pyautogui.moveTo(40, 75)
        pyautogui.click()
        time.sleep(2)

        wnd = win32ui.GetForegroundWindow()
        time.sleep(1)
        # pyautogui.press('tab')
        # time.sleep(1)
        # pyautogui.press('tab')
        # time.sleep(1)
        pyautogui.press('enter')

        # time.sleep(20)


        toplist = []
        winlist = []
        no_proceed = True

        t0 = time2()
        while no_proceed == True:
            if round(time2()-t0,2) > 90:
                print round(time2()-t0,2)
                print image_number, "took too long"
                make_error_email(image_number)
                make_sound(200,1000)
                sys.exit()

            win32gui.EnumWindows(enum_callback, toplist)
            page = [(hwnd, title) for hwnd, title in winlist if "Save As" in title]
            if len(page) > 0:
                time.sleep(1)
                page = page[0]
                win32gui.SetForegroundWindow(page[0])
                wnd = win32ui.GetForegroundWindow()
                time.sleep(1)
                document_name = "Document " + image_number
                pyautogui.typewrite(document_name, interval=.05)
                # pyautogui.hotkey('alt', 's')
                # print wnd.GetWindowText()
                pyautogui.press('enter')
        # error_check.append([image_number, 'Pass'])
                no_proceed = False

        t0 = time2()
        no_proceed = True
        while no_proceed == True:
            if round(time2()-t0,2) > 90:
                print round(time2()-t0,2)
                print image_number, "took too long"
                make_error_email(image_number)
                make_sound(200,1000)
                sys.exit()
            win32gui.EnumWindows(enum_callback, toplist)
            page = [(hwnd, title) for hwnd, title in winlist if "PDF-XChange Editor" in title]
            if len(page) > 0:
                time.sleep(1)
                page = page[0]
                win32gui.SetForegroundWindow(page[0])
                time.sleep(1)
                # wnd = win32ui.GetForegroundWindow()
                # print wnd.GetWindowText()
                win32gui.PostMessage(page[0],win32con.WM_CLOSE,0,0)
                no_proceed = False
                time.sleep(1)

    except Exception as e:
        print e
        make_error_email(image_number)
        make_sound(200,1000)
        sys.exit()
# print error_check
make_sound(200,1000)
make_completion_email()