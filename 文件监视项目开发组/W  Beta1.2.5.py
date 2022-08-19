import wx
import os
import threading
import time
import shutil
class SystemSettings(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, '文件监测备份系统',
                          size=(900, 680))
        self.SetMaxSize((900, 680))
        self.SetMinSize((900, 680))
        self.WindowRecord = 0
        self.font001 = wx.Font(19, wx.MODERN, wx.NORMAL, wx.NORMAL, False, 'Consolas') 
        self.panel = wx.Panel(self, -1)
        bmp1 = wx.Image('back.bmp', wx.BITMAP_TYPE_BMP).ConvertToBitmap( )
        self.ImageButten1 = wx.BitmapButton(self.panel, -1, bmp1, pos=(10, 560))
        bmp2 = wx.Image('forward.bmp', wx.BITMAP_TYPE_BMP).ConvertToBitmap( )
        self.ImageButten2 = wx.BitmapButton(self.panel, -1, bmp2, pos=(815, 560))
        self.ImageButten2.Bind(wx.EVT_BUTTON, self.Next)
        self.ImageButten1.Bind(wx.EVT_BUTTON, self.Last)
        self.button001 = wx.Button(self.panel,-1,"停止监测", size = (120, 60), pos = (3850, 560))
        self.button000 = wx.Button(self.panel,-1,"开始监测", size = (120, 60), pos = (385, 560))
        self.EntryText0001 = wx.TextCtrl(self.panel, -1, size=(100, -1), pos = (61000, 9500))
        self.button000.Bind(wx.EVT_BUTTON,self.PressStart)
        self.button001.Bind(wx.EVT_BUTTON,self.PressStop)
        self.button001.SetFont(self.font001)
        self.button000.SetFont(self.font001)
        self.StartUpStatePage()
        self.StateCode = 0
        self.LastSettingState = []
        self.WorkingState = True
        self.InitializationState = False
    def Initialization(self, originalpath, copypath, SelectCode = '', Monitormode = 0):
        FormatDic = {0:'all', 1:'txt', 2:'wma.wmv.rm.rmvb.aac.mid.wav.vqf.avi.cda',
                     3:'avi.rmvb.rm.asf.divx.mpg.mpeg.mpe.wmv.mp4.mkv.vob',
                     4:'bmp.jpg.jpeg.png.gif', 5:'ppt.pptx', 6:'xls.xlsx',
                     7:'doc.docx', 8:'mdb.db.mdf.dbf', 9:'reg'}
        self.originalpath = originalpath
        self.copypath = copypath
        self.Newfilepath = os.path.join(copypath, '新文件')
        self.Deletedfilepath = os.path.join(copypath, '已删除文件')
        self.Changedfilepath = os.path.join(copypath, '被更改文件')
        self.Openedfilepath = os.path.join(copypath, '被访问文件')
        self.backupfilepath = os.path.join(copypath, '备份路径')
        if os.path.exists(self.Newfilepath) == False:
            os.makedirs(self.Newfilepath)
        if os.path.exists(self.Deletedfilepath) == False:
            os.makedirs(self.Deletedfilepath)
        if os.path.exists(self.Changedfilepath) == False:
            os.makedirs(self.Changedfilepath)
        if os.path.exists(self.Openedfilepath) == False:
            os.makedirs(self.Openedfilepath)
        if os.path.exists(self.backupfilepath) == False:
            os.makedirs(self.backupfilepath)
        self.originalfilepath = self._listdir(self.originalpath)
        self._copyfilesinlist(self.originalfilepath, self.backupfilepath)
        self.filenames = []
        self.filesizes = [[]]
        self.fileopenedtime = [[]]
        self.filechangedtime = [[]]
        self.copyrecord = []
        self.filenames.append(self._listdir(self.originalpath))
        for element in self.filenames[-1]:
            fileinfo = os.stat(element)
            self.filesizes[-1].append(self._formatbyte(fileinfo.st_size))
            self.fileopenedtime[-1].append(self._formattime(fileinfo.st_atime))
            self.filechangedtime[-1].append(self._formattime(fileinfo.st_mtime))
        self.mode = Monitormode
    def AutoClean(self):
        if len(self.filenames) > 50:
            self.filenames = self.filenames[-3:]
            self.filesizes = self.filesizes[-3:]
            self.fileopenedtime = self.fileopenedtime[-3:]
            self.filechangedtime = self.filechangedtime[-3:]
            print('cleaned')
    def GetCopyRecord(self, event):
        if self.InitializationState == False:
            pass
        else:
            return self.copyrecord
    def _copyfilesinlistwithtime(self, inputlist, mode):
        modedic = {0:self.copypath, 1:self.Newfilepath, 2:self.Deletedfilepath,
        3:self.Openedfilepath, 4:self.Changedfilepath}
        path = modedic[mode]
        for element in inputlist:
            name = os.path.split(element)[1]
            currenttime = time.strftime('%Y-%m-%d %H-%M-%S', time.localtime())
            for index in range(len(name)):
                if name[len(name) - index - 1] == '.':
                    tempstr = name[len(name) - index - 1 : ]
                    name = name[ : len(name) - index - 1]
                    name = name + '[' + currenttime + ']' + str(mode) + tempstr
                    break
            target = os.path.join(path, name)
            shutil.copyfile(element, target)
            fileinfo = os.stat(target)
            sizes = self._formatbyte(fileinfo.st_size)
            target = target + ':' + sizes
            self.copyrecord.append(target)
            print(target)
    def _formatbyte(self, inputsize):
        for (size, standard) in [(1024 ** 3, 'GB'), (1024 ** 2, 'MB'), (1024, 'KB')]:
            if inputsize >= size:
                return '%.2f %s'%(inputsize / size, standard)
            elif inputsize == 1:
                return '1字节'
            else:
                byte = '%.2f'%(inputsize or 0)
        return (byte[: 3] if byte.endswith('.00') else byte) + '字节'
    def _copyfilesinlist(self, inputlist, path):
        if path == 0:
            path = self.copypath
        for element in inputlist:
            name = os.path.split(element)[1]
            target =os.path.join(path, name)
            shutil.copyfile(element, target)
    def _formattime(self, times):
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(times))
    def _shiftfilepaths(self, inputlist, targetpath):
        templist = []
        for element in inputlist:
            filename = os.path.split(element)[1]
            target = os.path.join(targetpath, filename)
            templist.append(target)
        return templist
    def _listdir(self, incomepath):
        templist = []
        for element_one in os.walk(incomepath):
            if len(element_one[1]) == 0 and len(element_one[2]) != 0:
                for element_two in element_one[2]:
                    abspath = os.path.join(element_one[0], element_two)
                    templist.append(abspath)
        return templist
    def ActiveScan(self, sleeptime = 0.5):
        while True:
            t1 = time.time()
            self.AutoClean()
            try:
                self.EntryText0001.GetValue()
            except RuntimeError:
                break
            self.filenames.append(self._listdir(self.originalpath))
            self.filesizes.append([])
            self.filechangedtime.append([])
            self.fileopenedtime.append([])
            self.t229 = str(len(self.filenames[-1]))
            for element in self.filenames[-1]:
                fileinfo = os.stat(element)
                self.filesizes[-1].append(self._formatbyte(fileinfo.st_size))
                self.fileopenedtime[-1].append(self._formattime(fileinfo.st_atime))
                self.filechangedtime[-1].append(self._formattime(fileinfo.st_mtime))
            self._AnalysisData()
            t2 = time.time()
            self.t230 = str(round((t2 - t1), 2))
            self.t230 += '秒/次'
            print(self.t230)
            time.sleep(sleeptime)
    def _AnalysisData(self):
        newfiles = []
        deletedfiles = []
        changedfiles = []
        openedfiles = []
        for element in self.filenames[-1]:
            if element not in self.filenames[-2]:
                newfiles.append(element)
        for element in self.filenames[-2]:
            if element not in self.filenames[-1]:
                deletedfiles.append(element)
        for index1 in range(len(self.filenames[-1])):
            for index2 in range(len(self.filenames[-2])):
               if self.filenames[-1][index1] == self.filenames[-2][index2]:
                   if self.filechangedtime[-1][index1] != self.filechangedtime[-2][index2]:
                       changedfiles.append(self.filenames[-1][index1])
                   if self.fileopenedtime[-1][index1] == self.fileopenedtime[-2][index2]:
                       openedfiles.append(self.filenames[-1][index1])
        self._copyfilesinlist(newfiles, self.backupfilepath)
        self._copyfilesinlist(changedfiles, self.backupfilepath)
        if self.mode == 0 or self.mode == 1:
            self._copyfilesinlistwithtime(newfiles, 1)
        if self.mode == 0 or self.mode == 2:
            deletedfiles = self._shiftfilepaths(deletedfiles, self.backupfilepath)
            self._copyfilesinlistwithtime(deletedfiles, 2)
        if self.mode == 0 or self.mode == 4:
            self._copyfilesinlistwithtime(changedfiles, 4)
        if self.mode == 3:
            self._copyfilesinlistwithtime(openedfiles, 3)
    def StartUpStatePage(self):
        X_Distance = 45
        Y_Distance = 15
        self.StatePage = wx.Choice(self.panel, -1, size = (90, 50), pos = (X_Distance + 2800, Y_Distance + 650), choices=['',''])
        self.bmp4 = wx.Image('BottomLine.bmp', wx.BITMAP_TYPE_BMP).ConvertToBitmap( )
        self.bmp5 = wx.Image('SideLine.bmp', wx.BITMAP_TYPE_BMP).ConvertToBitmap( )
        self.bmp6 = wx.Image('ToolLine.bmp', wx.BITMAP_TYPE_BMP).ConvertToBitmap( )
        self.font221 = wx.Font(19, wx.MODERN, wx.NORMAL, wx.NORMAL, False, 'Consolas') 
        self.font222 = wx.Font(15, wx.MODERN, wx.NORMAL, wx.NORMAL, False, 'Consolas')
        self.font223 = wx.Font(12, wx.MODERN, wx.NORMAL, wx.NORMAL, False, 'Consolas')
        self.font224 = wx.Font(10, wx.MODERN, wx.NORMAL, wx.NORMAL, False, 'Consolas')
        self.t221 = '监视器状态'
        self.t222 = '备份区容量使用情况'
        self.t223 = '正常运行时间:'
        self.t224 = '备份文件数量:'
        self.t225 = '备份文件大小:'
        self.t226 = '文件类型数目:'
        self.t227 = '当前扫描速度:'
        self.t228 = '监测中的文件数:'
        self.t229 = ''
        self.t230 = ''
        self.t231 = ''
        self.t232 = ''
        self.text221 = wx.StaticText(self.panel, -1, self.t221, size = (25,25), pos = (X_Distance + 315, Y_Distance + 15))
        self.DrawStateMap6 = wx.StaticBitmap(self.panel, -1, self.bmp5, (X_Distance + 733, Y_Distance + 65))
        self.DrawStateMap2 = wx.StaticBitmap(self.panel, -1, self.bmp5, (X_Distance + 54, Y_Distance + 65))
        self.DrawStateMap3 = wx.StaticBitmap(self.panel, -1, self.bmp6, (X_Distance + 485, Y_Distance + 65))
        self.DrawStateMap4 = wx.StaticBitmap(self.panel, -1, self.bmp4, (X_Distance + 54, Y_Distance + 498))
        self.DrawStateMap5 = wx.StaticBitmap(self.panel, -1, self.bmp4, (X_Distance + 56, Y_Distance + 356))
        self.DrawStateMap1 = wx.StaticBitmap(self.panel, -1, self.bmp4, (X_Distance + 54, Y_Distance + 65))
        self.text222 = wx.StaticText(self.panel, -1, self.t222, size = (25,25), pos = (X_Distance + 75, Y_Distance + 375))
        self.text223 = wx.StaticText(self.panel, -1, self.t223, pos = (X_Distance + 500, Y_Distance + 75))
        self.text224 = wx.StaticText(self.panel, -1, self.t224, pos = (X_Distance + 500, Y_Distance + 100))
        self.text225 = wx.StaticText(self.panel, -1, self.t225, pos = (X_Distance + 500, Y_Distance + 125))
        self.text226 = wx.StaticText(self.panel, -1, self.t226, pos = (X_Distance + 500, Y_Distance + 150))
        self.text227 = wx.StaticText(self.panel, -1, self.t227, pos = (X_Distance + 500, Y_Distance + 175))
        self.text228 = wx.StaticText(self.panel, -1, self.t228, pos = (X_Distance + 500, Y_Distance + 200))
        self.text229 = wx.StaticText(self.panel, -1, self.t229, pos = (45 + 645, 15 + 200))
        self.text230 = wx.StaticText(self.panel, -1, self.t230, pos = (45 + 625, 15 + 175))
        self.text221.SetFont(self.font221)
        self.text222.SetFont(self.font222)
        self.text223.SetFont(self.font223)
        self.text224.SetFont(self.font223)
        self.text225.SetFont(self.font223)
        self.text226.SetFont(self.font223)
        self.text227.SetFont(self.font223)
        self.text228.SetFont(self.font223)
        self.text229.SetFont(self.font223)
        self.text230.SetFont(self.font223)
        self.gauge = wx.Gauge(self.panel, range=100, pos=(X_Distance + 120, Y_Distance + 415), 
                              size=(540, 35))
        self.button11 = wx.Button(self.panel,-1,"打开备份文件夹", size = (105, 25), pos = (X_Distance + 615, Y_Distance + 465))
        threading.Timer(0.1, self.KeepUpDatingData).start()
    def KeepUpDatingData(self):
        while True:
            try:
                self.StatePage.GetSelection()
            except RuntimeError:
                break
            else:
                time.sleep(1)
                self.text229.Destroy()
                self.text229 = wx.StaticText(self.panel, -1, self.t229, size = (45, 25), pos = (45 + 645, 15 + 200))
                self.text229.SetFont(self.font223)
                self.text230.Destroy()
                self.text230 = wx.StaticText(self.panel, -1, self.t230, size = (105, 25), pos = (45 + 625, 15 + 175))
                self.text230.SetFont(self.font223)
    def DestroyFlieLists(self, event):
        if self.length >= 1:
            self.TextMatrix01.Destroy()
            self.TextMatrix11.Destroy()
            self.TextMatrix21.Destroy()
            self.TextMatrix31.Destroy()
            self.TextMatrix41.Destroy()
        if self.length >= 2:
            self.TextMatrix02.Destroy()
            self.TextMatrix12.Destroy()
            self.TextMatrix22.Destroy()
            self.TextMatrix32.Destroy()
            self.TextMatrix42.Destroy()
        if self.length >= 3:
            self.TextMatrix03.Destroy()
            self.TextMatrix13.Destroy()
            self.TextMatrix23.Destroy()
            self.TextMatrix33.Destroy()
            self.TextMatrix43.Destroy()
        if self.length >= 4:
            self.TextMatrix04.Destroy()
            self.TextMatrix14.Destroy()
            self.TextMatrix24.Destroy()
            self.TextMatrix34.Destroy()
            self.TextMatrix44.Destroy()
        if self.length >= 5:
            self.TextMatrix05.Destroy()
            self.TextMatrix15.Destroy()
            self.TextMatrix25.Destroy()
            self.TextMatrix35.Destroy()
            self.TextMatrix45.Destroy()
        if self.length >= 6:
            self.TextMatrix06.Destroy()
            self.TextMatrix16.Destroy()
            self.TextMatrix26.Destroy()
            self.TextMatrix36.Destroy()
            self.TextMatrix46.Destroy()
        if self.length >= 7:
            self.TextMatrix07.Destroy()
            self.TextMatrix17.Destroy()
            self.TextMatrix27.Destroy()
            self.TextMatrix37.Destroy()
            self.TextMatrix47.Destroy()
        if self.length >= 8:
            self.TextMatrix08.Destroy()
            self.TextMatrix18.Destroy()
            self.TextMatrix28.Destroy()
            self.TextMatrix38.Destroy()
            self.TextMatrix48.Destroy()
        if self.length >= 9:
            self.TextMatrix09.Destroy()
            self.TextMatrix19.Destroy()
            self.TextMatrix29.Destroy()
            self.TextMatrix39.Destroy()
            self.TextMatrix49.Destroy()
        if self.length >= 10:
            self.TextMatrix010.Destroy()
            self.TextMatrix110.Destroy()
            self.TextMatrix210.Destroy()
            self.TextMatrix310.Destroy()
            self.TextMatrix410.Destroy()
        if self.length >= 11:
            self.TextMatrix011.Destroy()
            self.TextMatrix111.Destroy()
            self.TextMatrix211.Destroy()
            self.TextMatrix311.Destroy()
            self.TextMatrix411.Destroy()
        if self.length >= 12:
            self.TextMatrix012.Destroy()
            self.TextMatrix112.Destroy()
            self.TextMatrix212.Destroy()
            self.TextMatrix312.Destroy()
            self.TextMatrix412.Destroy()
        if self.length >= 13:
            self.TextMatrix013.Destroy()
            self.TextMatrix113.Destroy()
            self.TextMatrix213.Destroy()
            self.TextMatrix313.Destroy()
            self.TextMatrix413.Destroy()
        if self.length >= 14:
            self.TextMatrix014.Destroy()
            self.TextMatrix114.Destroy()
            self.TextMatrix214.Destroy()
            self.TextMatrix314.Destroy()
            self.TextMatrix414.Destroy()
        if self.length >= 15:
            self.TextMatrix015.Destroy()
            self.TextMatrix115.Destroy()
            self.TextMatrix215.Destroy()
            self.TextMatrix315.Destroy()
            self.TextMatrix415.Destroy()
        if self.length >= 16:
            self.TextMatrix016.Destroy()
            self.TextMatrix116.Destroy()
            self.TextMatrix216.Destroy()
            self.TextMatrix316.Destroy()
            self.TextMatrix416.Destroy()
        if self.length >= 17:
            self.TextMatrix017.Destroy()
            self.TextMatrix117.Destroy()
            self.TextMatrix217.Destroy()
            self.TextMatrix317.Destroy()
            self.TextMatrix417.Destroy()
    def CutInto(self, InputData, CutLen = 17):
        Cutted_List = []
        Count = 0
        if InputData != None:
            for element in InputData:
                if Count % (CutLen) == 0:
                    Cutted_List.append([])
                Cutted_List[Count // (CutLen)].append(element)
                Count += 1
            return Cutted_List
    def ProcessNeededText(self, Index):
        self.MatrixText1 = os.path.split(self.InputList[Index].split(':')[1])[1]
        TextLen = 0
        TempTxt = ''
        for element in self.MatrixText1:
            if element.isalpha() == True:
                TextLen += 1
            if element.isalpha() == False:
                TextLen += 2
            if TextLen >= 30:
                TempTxt = TempTxt + '..' + self.MatrixText1[-4:]
                break
            TempTxt += element
        self.MatrixText1 = TempTxt
        self.MatrixText2 = self.InputList[Index].split(':')[2]
        self.MatrixText3 = self.InputList[Index].split('[')[1].split(']')[0][11:]
        self.MatrixText3 = self.MatrixText3.split('-')
        temp = self.MatrixText3[0]
        for element in self.MatrixText3[1:]:
            temp = temp + ':' + element
        self.MatrixText3 = temp
        self.MatrixText4 = self.Trig_EVT[self.InputList[Index].split('.')[0][-1]]
    def ShowFileLists(self, InputList):
        if InputList == None:
            self.length = 0
            return None
        self.InputList = InputList
        self.Trig_EVT  = {'1':'文件被创建', '2':'文件被删除', '4':'文件被修改'}
        self.length = len(InputList)
        self.MatrixFont = wx.Font(10, wx.MODERN, wx.NORMAL, wx.NORMAL, False, 'Consolas')
        self.MatrixText5 = '是'
        if self.length >= 1:
            self.ProcessNeededText(0)
            self.TextMatrix01 = wx.StaticText(self.panel, -1, self.MatrixText1, size = (0,0), pos = (95, 173))
            self.TextMatrix11 = wx.StaticText(self.panel, -1, self.MatrixText2, size = (0,0), pos = (370, 173))
            self.TextMatrix21 = wx.StaticText(self.panel, -1, self.MatrixText3, size = (0,0), pos = (470, 173))
            self.TextMatrix31 = wx.StaticText(self.panel, -1, self.MatrixText4, size = (0,0), pos = (566, 173))
            self.TextMatrix41 = wx.StaticText(self.panel, -1, self.MatrixText5, size = (0,0), pos = (688, 173))
            self.TextMatrix01.SetFont(self.MatrixFont)
            self.TextMatrix11.SetFont(self.MatrixFont)
            self.TextMatrix21.SetFont(self.MatrixFont)
            self.TextMatrix31.SetFont(self.MatrixFont)
            self.TextMatrix41.SetFont(self.MatrixFont)
        if self.length >= 2:
            self.ProcessNeededText(1)
            self.TextMatrix02 = wx.StaticText(self.panel, -1, self.MatrixText1, size = (0,0), pos = (95, 193))
            self.TextMatrix12 = wx.StaticText(self.panel, -1, self.MatrixText2, size = (0,0), pos = (370, 193))
            self.TextMatrix22 = wx.StaticText(self.panel, -1, self.MatrixText3, size = (0,0), pos = (470, 193))
            self.TextMatrix32 = wx.StaticText(self.panel, -1, self.MatrixText4, size = (0,0), pos = (566, 193))
            self.TextMatrix42 = wx.StaticText(self.panel, -1, self.MatrixText5, size = (0,0), pos = (688, 193))
            self.TextMatrix02.SetFont(self.MatrixFont)
            self.TextMatrix12.SetFont(self.MatrixFont)
            self.TextMatrix22.SetFont(self.MatrixFont)
            self.TextMatrix32.SetFont(self.MatrixFont)
            self.TextMatrix42.SetFont(self.MatrixFont)
        if self.length >= 3:
            self.ProcessNeededText(2)
            self.TextMatrix03 = wx.StaticText(self.panel, -1, self.MatrixText1, size = (0,0), pos = (95, 214))
            self.TextMatrix13 = wx.StaticText(self.panel, -1, self.MatrixText2, size = (0,0), pos = (370, 214))
            self.TextMatrix23 = wx.StaticText(self.panel, -1, self.MatrixText3, size = (0,0), pos = (470, 214))
            self.TextMatrix33 = wx.StaticText(self.panel, -1, self.MatrixText4, size = (0,0), pos = (566, 214))
            self.TextMatrix43 = wx.StaticText(self.panel, -1, self.MatrixText5, size = (0,0), pos = (688, 214))
            self.TextMatrix03.SetFont(self.MatrixFont)
            self.TextMatrix13.SetFont(self.MatrixFont)
            self.TextMatrix23.SetFont(self.MatrixFont)
            self.TextMatrix33.SetFont(self.MatrixFont)
            self.TextMatrix43.SetFont(self.MatrixFont)
        if self.length >= 4:
            self.ProcessNeededText(3)
            self.TextMatrix04 = wx.StaticText(self.panel, -1, self.MatrixText1, size = (0,0), pos = (95, 234))
            self.TextMatrix14 = wx.StaticText(self.panel, -1, self.MatrixText2, size = (0,0), pos = (370, 234))
            self.TextMatrix24 = wx.StaticText(self.panel, -1, self.MatrixText3, size = (0,0), pos = (470, 234))
            self.TextMatrix34 = wx.StaticText(self.panel, -1, self.MatrixText4, size = (0,0), pos = (566, 234))
            self.TextMatrix44 = wx.StaticText(self.panel, -1, self.MatrixText5, size = (0,0), pos = (688, 234))
            self.TextMatrix04.SetFont(self.MatrixFont)
            self.TextMatrix14.SetFont(self.MatrixFont)
            self.TextMatrix24.SetFont(self.MatrixFont)
            self.TextMatrix34.SetFont(self.MatrixFont)
            self.TextMatrix44.SetFont(self.MatrixFont)
        if self.length >= 5:
            self.ProcessNeededText(4)
            self.TextMatrix05 = wx.StaticText(self.panel, -1, self.MatrixText1, size = (0,0), pos = (95, 254))
            self.TextMatrix15 = wx.StaticText(self.panel, -1, self.MatrixText2, size = (0,0), pos = (370, 254))
            self.TextMatrix25 = wx.StaticText(self.panel, -1, self.MatrixText3, size = (0,0), pos = (470, 254))
            self.TextMatrix35 = wx.StaticText(self.panel, -1, self.MatrixText4, size = (0,0), pos = (566, 254))
            self.TextMatrix45 = wx.StaticText(self.panel, -1, self.MatrixText5, size = (0,0), pos = (688, 254))
            self.TextMatrix05.SetFont(self.MatrixFont)
            self.TextMatrix15.SetFont(self.MatrixFont)
            self.TextMatrix25.SetFont(self.MatrixFont)
            self.TextMatrix35.SetFont(self.MatrixFont)
            self.TextMatrix45.SetFont(self.MatrixFont)
        if self.length >= 6:
            self.ProcessNeededText(5)
            self.TextMatrix06 = wx.StaticText(self.panel, -1, self.MatrixText1, size = (0,0), pos = (95, 274))
            self.TextMatrix16 = wx.StaticText(self.panel, -1, self.MatrixText2, size = (0,0), pos = (370, 274))
            self.TextMatrix26 = wx.StaticText(self.panel, -1, self.MatrixText3, size = (0,0), pos = (470, 274))
            self.TextMatrix36 = wx.StaticText(self.panel, -1, self.MatrixText4, size = (0,0), pos = (566, 274))
            self.TextMatrix46 = wx.StaticText(self.panel, -1, self.MatrixText5, size = (0,0), pos = (688, 274))
            self.TextMatrix06.SetFont(self.MatrixFont)
            self.TextMatrix16.SetFont(self.MatrixFont)
            self.TextMatrix26.SetFont(self.MatrixFont)
            self.TextMatrix36.SetFont(self.MatrixFont)
            self.TextMatrix46.SetFont(self.MatrixFont)
        if self.length >= 7:
            self.ProcessNeededText(6)
            self.TextMatrix07 = wx.StaticText(self.panel, -1, self.MatrixText1, size = (0,0), pos = (95, 294))
            self.TextMatrix17 = wx.StaticText(self.panel, -1, self.MatrixText2, size = (0,0), pos = (370, 294))
            self.TextMatrix27 = wx.StaticText(self.panel, -1, self.MatrixText3, size = (0,0), pos = (470, 294))
            self.TextMatrix37 = wx.StaticText(self.panel, -1, self.MatrixText4, size = (0,0), pos = (566, 294))
            self.TextMatrix47 = wx.StaticText(self.panel, -1, self.MatrixText5, size = (0,0), pos = (688, 294))
            self.TextMatrix07.SetFont(self.MatrixFont)
            self.TextMatrix17.SetFont(self.MatrixFont)
            self.TextMatrix27.SetFont(self.MatrixFont)
            self.TextMatrix37.SetFont(self.MatrixFont)
            self.TextMatrix47.SetFont(self.MatrixFont)
        if self.length >= 8:
            self.ProcessNeededText(7)
            self.TextMatrix08 = wx.StaticText(self.panel, -1, self.MatrixText1, size = (0,0), pos = (95, 314))
            self.TextMatrix18 = wx.StaticText(self.panel, -1, self.MatrixText2, size = (0,0), pos = (370, 314))
            self.TextMatrix28 = wx.StaticText(self.panel, -1, self.MatrixText3, size = (0,0), pos = (470, 314))
            self.TextMatrix38 = wx.StaticText(self.panel, -1, self.MatrixText4, size = (0,0), pos = (566, 314))
            self.TextMatrix48 = wx.StaticText(self.panel, -1, self.MatrixText5, size = (0,0), pos = (688, 314))
            self.TextMatrix08.SetFont(self.MatrixFont)
            self.TextMatrix18.SetFont(self.MatrixFont)
            self.TextMatrix28.SetFont(self.MatrixFont)
            self.TextMatrix38.SetFont(self.MatrixFont)
            self.TextMatrix48.SetFont(self.MatrixFont)
        if self.length >= 9:
            self.ProcessNeededText(8)
            self.TextMatrix09 = wx.StaticText(self.panel, -1, self.MatrixText1, size = (0,0), pos = (95, 334))
            self.TextMatrix19 = wx.StaticText(self.panel, -1, self.MatrixText2, size = (0,0), pos = (370, 334))
            self.TextMatrix29 = wx.StaticText(self.panel, -1, self.MatrixText3, size = (0,0), pos = (470, 334))
            self.TextMatrix39 = wx.StaticText(self.panel, -1, self.MatrixText4, size = (0,0), pos = (566, 334))
            self.TextMatrix49 = wx.StaticText(self.panel, -1, self.MatrixText5, size = (0,0), pos = (688, 334))
            self.TextMatrix09.SetFont(self.MatrixFont)
            self.TextMatrix19.SetFont(self.MatrixFont)
            self.TextMatrix29.SetFont(self.MatrixFont)
            self.TextMatrix39.SetFont(self.MatrixFont)
            self.TextMatrix49.SetFont(self.MatrixFont)
        if self.length >= 10:
            self.ProcessNeededText(9)
            self.TextMatrix010 = wx.StaticText(self.panel, -1, self.MatrixText1, size = (0,0), pos = (95, 354))
            self.TextMatrix110 = wx.StaticText(self.panel, -1, self.MatrixText2, size = (0,0), pos = (370, 354))
            self.TextMatrix210 = wx.StaticText(self.panel, -1, self.MatrixText3, size = (0,0), pos = (470, 354))
            self.TextMatrix310 = wx.StaticText(self.panel, -1, self.MatrixText4, size = (0,0), pos = (566, 354))
            self.TextMatrix410 = wx.StaticText(self.panel, -1, self.MatrixText5, size = (0,0), pos = (688, 354))
            self.TextMatrix010.SetFont(self.MatrixFont)
            self.TextMatrix110.SetFont(self.MatrixFont)
            self.TextMatrix210.SetFont(self.MatrixFont)
            self.TextMatrix310.SetFont(self.MatrixFont)
            self.TextMatrix410.SetFont(self.MatrixFont)
        if self.length >= 11:
            self.ProcessNeededText(10)
            self.TextMatrix011 = wx.StaticText(self.panel, -1, self.MatrixText1, size = (0,0), pos = (95, 374))
            self.TextMatrix111 = wx.StaticText(self.panel, -1, self.MatrixText2, size = (0,0), pos = (370, 374))
            self.TextMatrix211 = wx.StaticText(self.panel, -1, self.MatrixText3, size = (0,0), pos = (470, 374))
            self.TextMatrix311 = wx.StaticText(self.panel, -1, self.MatrixText4, size = (0,0), pos = (566, 374))
            self.TextMatrix411 = wx.StaticText(self.panel, -1, self.MatrixText5, size = (0,0), pos = (688, 374))
            self.TextMatrix011.SetFont(self.MatrixFont)
            self.TextMatrix111.SetFont(self.MatrixFont)
            self.TextMatrix211.SetFont(self.MatrixFont)
            self.TextMatrix311.SetFont(self.MatrixFont)
            self.TextMatrix411.SetFont(self.MatrixFont)
        if self.length >= 12:
            self.ProcessNeededText(11)
            self.TextMatrix012 = wx.StaticText(self.panel, -1, self.MatrixText1, size = (0,0), pos = (95, 394))
            self.TextMatrix112 = wx.StaticText(self.panel, -1, self.MatrixText2, size = (0,0), pos = (370, 394))
            self.TextMatrix212 = wx.StaticText(self.panel, -1, self.MatrixText3, size = (0,0), pos = (470, 394))
            self.TextMatrix312 = wx.StaticText(self.panel, -1, self.MatrixText4, size = (0,0), pos = (566, 394))
            self.TextMatrix412 = wx.StaticText(self.panel, -1, self.MatrixText5, size = (0,0), pos = (688, 394))
            self.TextMatrix012.SetFont(self.MatrixFont)
            self.TextMatrix112.SetFont(self.MatrixFont)
            self.TextMatrix212.SetFont(self.MatrixFont)
            self.TextMatrix312.SetFont(self.MatrixFont)
            self.TextMatrix412.SetFont(self.MatrixFont)
        if self.length >= 13:
            self.ProcessNeededText(12)
            self.TextMatrix013 = wx.StaticText(self.panel, -1, self.MatrixText1, size = (0,0), pos = (95, 414))
            self.TextMatrix113 = wx.StaticText(self.panel, -1, self.MatrixText2, size = (0,0), pos = (370, 414))
            self.TextMatrix213 = wx.StaticText(self.panel, -1, self.MatrixText3, size = (0,0), pos = (470, 414))
            self.TextMatrix313 = wx.StaticText(self.panel, -1, self.MatrixText4, size = (0,0), pos = (566, 414))
            self.TextMatrix413 = wx.StaticText(self.panel, -1, self.MatrixText5, size = (0,0), pos = (688, 414))
            self.TextMatrix013.SetFont(self.MatrixFont)
            self.TextMatrix113.SetFont(self.MatrixFont)
            self.TextMatrix213.SetFont(self.MatrixFont)
            self.TextMatrix313.SetFont(self.MatrixFont)
            self.TextMatrix413.SetFont(self.MatrixFont)
        if self.length >= 14:
            self.ProcessNeededText(13)
            self.TextMatrix014 = wx.StaticText(self.panel, -1, self.MatrixText1, size = (0,0), pos = (95, 434))
            self.TextMatrix114 = wx.StaticText(self.panel, -1, self.MatrixText2, size = (0,0), pos = (370, 434))
            self.TextMatrix214 = wx.StaticText(self.panel, -1, self.MatrixText3, size = (0,0), pos = (470, 434))
            self.TextMatrix314 = wx.StaticText(self.panel, -1, self.MatrixText4, size = (0,0), pos = (566, 434))
            self.TextMatrix414 = wx.StaticText(self.panel, -1, self.MatrixText5, size = (0,0), pos = (688, 434))
            self.TextMatrix014.SetFont(self.MatrixFont)
            self.TextMatrix114.SetFont(self.MatrixFont)
            self.TextMatrix214.SetFont(self.MatrixFont)
            self.TextMatrix314.SetFont(self.MatrixFont)
            self.TextMatrix414.SetFont(self.MatrixFont)
        if self.length >= 15:
            self.ProcessNeededText(14)
            self.TextMatrix015 = wx.StaticText(self.panel, -1, self.MatrixText1, size = (0,0), pos = (95, 454))
            self.TextMatrix115 = wx.StaticText(self.panel, -1, self.MatrixText2, size = (0,0), pos = (370, 454))
            self.TextMatrix215 = wx.StaticText(self.panel, -1, self.MatrixText3, size = (0,0), pos = (470, 454))
            self.TextMatrix315 = wx.StaticText(self.panel, -1, self.MatrixText4, size = (0,0), pos = (566, 454))
            self.TextMatrix415 = wx.StaticText(self.panel, -1, self.MatrixText5, size = (0,0), pos = (688, 454))
            self.TextMatrix015.SetFont(self.MatrixFont)
            self.TextMatrix115.SetFont(self.MatrixFont)
            self.TextMatrix215.SetFont(self.MatrixFont)
            self.TextMatrix315.SetFont(self.MatrixFont)
            self.TextMatrix415.SetFont(self.MatrixFont)
        if self.length >= 16:
            self.ProcessNeededText(15)
            self.TextMatrix016 = wx.StaticText(self.panel, -1, self.MatrixText1, size = (0,0), pos = (95, 474))
            self.TextMatrix116 = wx.StaticText(self.panel, -1, self.MatrixText2, size = (0,0), pos = (370, 474))
            self.TextMatrix216 = wx.StaticText(self.panel, -1, self.MatrixText3, size = (0,0), pos = (470, 474))
            self.TextMatrix316 = wx.StaticText(self.panel, -1, self.MatrixText4, size = (0,0), pos = (566, 474))
            self.TextMatrix416 = wx.StaticText(self.panel, -1, self.MatrixText5, size = (0,0), pos = (688, 474))
            self.TextMatrix016.SetFont(self.MatrixFont)
            self.TextMatrix116.SetFont(self.MatrixFont)
            self.TextMatrix216.SetFont(self.MatrixFont)
            self.TextMatrix316.SetFont(self.MatrixFont)
            self.TextMatrix416.SetFont(self.MatrixFont)
        if self.length >= 17:
            self.ProcessNeededText(16)
            self.TextMatrix017 = wx.StaticText(self.panel, -1, self.MatrixText1, size = (0,0), pos = (95, 492))
            self.TextMatrix117 = wx.StaticText(self.panel, -1, self.MatrixText2, size = (0,0), pos = (370, 492))
            self.TextMatrix217 = wx.StaticText(self.panel, -1, self.MatrixText3, size = (0,0), pos = (470, 492))
            self.TextMatrix317 = wx.StaticText(self.panel, -1, self.MatrixText4, size = (0,0), pos = (566, 492))
            self.TextMatrix417 = wx.StaticText(self.panel, -1, self.MatrixText5, size = (0,0), pos = (688, 492))
            self.TextMatrix017.SetFont(self.MatrixFont)
            self.TextMatrix117.SetFont(self.MatrixFont)
            self.TextMatrix217.SetFont(self.MatrixFont)
            self.TextMatrix317.SetFont(self.MatrixFont)
            self.TextMatrix417.SetFont(self.MatrixFont)
        
    def DestroyStatePage(self):
        self.text221.Destroy()
        self.text222.Destroy()
        self.text223.Destroy()
        self.text224.Destroy()
        self.text225.Destroy()
        self.text226.Destroy()
        self.text227.Destroy()
        self.text228.Destroy()
        self.DrawStateMap1.Destroy()
        self.DrawStateMap2.Destroy()
        self.DrawStateMap3.Destroy()
        self.DrawStateMap4.Destroy()
        self.DrawStateMap5.Destroy()
        self.DrawStateMap6.Destroy()
        self.gauge.Destroy()
        self.button11.Destroy()
    def PressStart(self, event):
        if self.InitializationState == False:
            InFo1 = wx.MessageDialog(None,"未对监视器初始化，进行初始设置，请转到系统设置界面,设置完成后点击保存", "错误")
            if InFo1.ShowModal() == wx.ID_YES:
                InFo1.Destroy()
        else:
            self.button000.Destroy()
            self.button001 = wx.Button(self.panel,-1,"停止监测", size = (120, 60), pos = (385, 560))
            self.button001.SetFont(self.font001)
            self.button001.Bind(wx.EVT_BUTTON,self.PressStop)
            self.EntryText0001 = wx.TextCtrl(self.panel, -1, size=(100, -1), pos = (61000, 9500))
            threading.Timer(0.11, self.ActiveScan).start()

        
    def PressStop(self, event):
        try:
            self.EntryText0001.Destroy()
        except RuntimeError:
            pass
        else:
            pass
        finally:
            self.button001.Destroy()
            self.button000 = wx.Button(self.panel,-1,"开始监测", size = (120, 60), pos = (385, 560))
            self.button000.SetFont(self.font001)
            self.button000.Bind(wx.EVT_BUTTON,self.PressStart)
    def Last(self, event):
        if self.StateCode == 0:
            pass
        if self.StateCode == 1:
            self.DestroyMonitorSettings(0)
            self.StartUpStatePage()
            self.StateCode -= 1
            return None
        if self.StateCode == 2:
            self.DestroySystemSettings(0)
            self.StartUpMonitorSettings(0)
            self.StateCode -= 1
    def Next(self, event):
        if self.StateCode == 0:
            self.StatePage.Destroy()
            self.DestroyStatePage()
            self.StartUpMonitorSettings(0)
            self.StateCode += 1
            return None
        if self.StateCode == 1:
            self.DestroyMonitorSettings(0)
            self.StartUpSystemSettings(0)
            self.StateCode += 1
            if len(self.LastSettingState) != 0:
                self.BackSettings()
            return None
        if self.StateCode == 2:
            pass
    def DestroyMonitorSettings(self, event):
        self.font01.Destroy()
        self.font02.Destroy()
        self.font03.Destroy()
        self.font04.Destroy()
        self.text01.Destroy()
        self.text02.Destroy()
        self.text03.Destroy()
        self.text04.Destroy()
        self.text05.Destroy()
        self.text06.Destroy()
        self.text07.Destroy()
        self.text08.Destroy()
        self.DrawMonitorList.Destroy()
        self.listbox01.Destroy()
        self.listbox02.Destroy()
        self.listbox03.Destroy()
        self.butten01.Destroy()
        self.butten02.Destroy()
        self.butten03.Destroy()
        self.DestroyFlieLists(0)
    def StartUpMonitorSettings(self, event):
        self.bmp3 = wx.Image('FormOutput1.bmp', wx.BITMAP_TYPE_BMP).ConvertToBitmap( )
        X_Distance = 50
        Y_Distance = 30
        self.font01 = wx.Font(19, wx.MODERN, wx.NORMAL, wx.NORMAL, False, 'Consolas') 
        self.font02 = wx.Font(15, wx.MODERN, wx.NORMAL, wx.NORMAL, False, 'Consolas')
        self.font03 = wx.Font(12, wx.MODERN, wx.NORMAL, wx.NORMAL, False, 'Consolas')
        self.font04 = wx.Font(10, wx.MODERN, wx.NORMAL, wx.NORMAL, False, 'Consolas')
        self.t01 = '文件筛选器'
        self.t02 = '筛选条件'
        self.t03 = '---------------------------------------------------'
        self.t04 = '类型:'
        self.t05 = '排序:'
        self.t06 = '触发类型:'
        self.text03 = wx.StaticText(self.panel, -1, self.t03, size = (0,0), pos = (X_Distance + 30, Y_Distance + 90))
        self.text07 = wx.StaticText(self.panel, -1, self.t03, size = (0,0), pos = (X_Distance + 30, Y_Distance + 481))
        self.text01 = wx.StaticText(self.panel, -1, self.t01, size = (25,25), pos = (X_Distance + 315, Y_Distance + 0))
        self.text02 = wx.StaticText(self.panel, -1, self.t02, size = (25,25), pos = (X_Distance + 45, Y_Distance + 65))
        self.text04 = wx.StaticText(self.panel, -1, self.t04, size = (25,25), pos = (X_Distance + 225, Y_Distance + 68))
        self.text05 = wx.StaticText(self.panel, -1, self.t05, size = (25,25), pos = (X_Distance + 395, Y_Distance + 68))
        self.text06 = wx.StaticText(self.panel, -1, self.t06, size = (25,25), pos = (X_Distance + 555, Y_Distance + 68))
        self.text01.SetFont(self.font01)
        self.text02.SetFont(self.font02)
        self.text03.SetFont(self.font01)
        self.text04.SetFont(self.font03)
        self.text05.SetFont(self.font03)
        self.text06.SetFont(self.font03)
        self.text07.SetFont(self.font01)
        self.DrawMonitorList = wx.StaticBitmap(self.panel, -1, self.bmp3, (X_Distance + 38, Y_Distance + 120), (self.bmp3.GetWidth(), self.bmp3.GetHeight()))
        self.List01 = ['全部', '记事本文件', '音频', '视频', '图片', '幻灯片', '表格',
                      '文档', '数据库文件', '注册表文件', '图标',
                      '快捷方式']
        self.List02 = ['按时间降序', '按时间升序', '按大小升序', '按大小降序', '默认排序']
        self.List03 = ['全部', '被删除', '被更改', '被创建']
        self.listbox01 = wx.Choice(self.panel, -1, size = (90, 50), pos = (X_Distance + 280, Y_Distance + 65), choices=self.List01)
        self.listbox02 = wx.Choice(self.panel, -1, size = (85, 50), pos = (X_Distance + 450, Y_Distance + 65), choices=self.List02)
        self.listbox03 = wx.Choice(self.panel, -1, size = (80, 50), pos = (X_Distance + 655, Y_Distance + 65), choices=self.List03)
        self.butten01 = wx.Button(self.panel,-1,"下一页", size = (50, 25), pos = (X_Distance + 605, Y_Distance + 510))
        self.butten02 = wx.Button(self.panel,-1,"上一页", size = (50, 25), pos = (X_Distance + 505, Y_Distance + 510))
        self.butten03 = wx.Button(self.panel,-1,"刷新界面", size = (60, 25), pos = (X_Distance + 685, Y_Distance + 510))
        self.FirstList = []
        self.butten01.Bind(wx.EVT_BUTTON, self.NextPage)
        self.butten02.Bind(wx.EVT_BUTTON, self.LastPage)
        self.butten03.Bind(wx.EVT_BUTTON, self.RefreshMonitorSettings)
        self.listbox01.SetSelection(0)
        self.listbox02.SetSelection(4)
        self.listbox03.SetSelection(0)
        self.CurrentPage = 0
        self.DataList = self.GetCopyRecord(0)
        self.length = 0
        self.cur = 0
        self.total = 0
        self.Cutted = self.CutInto(self.DataList)
        if self.Cutted == None:
            self.t07 = '0/0页'
        else:
            self.total = len(self.Cutted)
            self.t07 = f'{self.CurrentPage + 1}/{self.total}页'
        self.text08 = wx.StaticText(self.panel, -1, self.t07, size = (0,0), pos = (X_Distance + 560, Y_Distance + 512))
        self.text08.SetFont(self.font03)
        if self.Cutted != None and self.Cutted != []:
            self.ShowFileLists(self.Cutted[self.CurrentPage])
        else:
            self.ShowFileLists(self.Cutted)
    def RefreshMonitorSettings(self, event):
        self.text08.Destroy()
        self.DataList = self.GetCopyRecord(0)
        self.length = 0
        self.total = 0
        self.Cutted = self.CutInto(self.DataList)
        if self.Cutted == None:
            self.t07 = '0/0页'
        else:
            self.total = len(self.Cutted)
            self.t07 = f'{self.CurrentPage + 1}/{self.total}页'
        self.text08 = wx.StaticText(self.panel, -1, self.t07, size = (0,0), pos = (50 + 560, 30 + 512))
        self.text08.SetFont(self.font03)
        if self.Cutted != None and self.Cutted != []:
            self.ShowFileLists(self.Cutted[self.CurrentPage])
        else:
            self.ShowFileLists(self.Cutted)
    def LastPage(self, event):
        if self.CurrentPage > 0:
            self.CurrentPage -= 1
            self.DestroyFlieLists(0)
            self.ShowFileLists(self.Cutted[self.CurrentPage])
            self.text08.Destroy()
            self.t07 = f'{self.CurrentPage + 1}/{self.total}页'
            self.text08 = wx.StaticText(self.panel, -1, self.t07, size = (0,0), pos = (50 + 560, 30 + 512))
            self.text08.SetFont(self.font03)
    def NextPage(self, event):
        if self.CurrentPage < len(self.Cutted) - 1:
            self.CurrentPage += 1
            self.DestroyFlieLists(0)
            self.ShowFileLists(self.Cutted[self.CurrentPage])
            self.text08.Destroy()
            self.t07 = f'{self.CurrentPage + 1}/{self.total}页'
            self.text08 = wx.StaticText(self.panel, -1, self.t07, size = (0,0), pos = (50 + 560, 30 + 512))
            self.text08.SetFont(self.font03)
    def StartUpSystemSettings(self, event):
        Y_Distance = 10
        X_Distance = 55
        bmp1 = wx.Image('back.bmp', wx.BITMAP_TYPE_BMP).ConvertToBitmap( )
        self.ImageButten1 = wx.BitmapButton(self.panel, -1, bmp1, pos=(10, 560))
        bmp2 = wx.Image('forward.bmp', wx.BITMAP_TYPE_BMP).ConvertToBitmap( )
        self.ImageButten2 = wx.BitmapButton(self.panel, -1, bmp2, pos=(815, 560))
        self.t1 = '监视设置'
        self.t2 = '文件设置'
        self.t3 = '高级设置'
        self.t4 = '系统设置'
        self.t5 = '-----------------------------------------------------------------'
        self.t6 = '目标筛选'
        self.t7 = '备份动作触发条件:'
        self.t8 = '监视目录选择:'
        self.t9 = '硬盘备份区大小限制:'
        self.t10 = '当备份区将满时:'
        self.t11 = '备份文件存放路径:'
        self.t12 = 'CPU使用率限制:'
        self.t13 = '内存使用限制:'
        self.t14 = '开启多线程加速'
        self.t15 = '开启内存缓冲加速'
        self.t16 = '设置内存缓冲区大小:'
        self.t17 = '在此输入后缀:'
        self.t18 = '<= 文件大小 <='
        self.t19 = '单位'
        self.t20 = '文件名:'
        self.t21 = '%'
        self.t22 = 'MB'
        self.text1 = wx.StaticText(self.panel, -1, self.t1, size = (25,50), pos = (X_Distance + 10, Y_Distance + 40))
        self.text2 = wx.StaticText(self.panel, -1, self.t2, size = (25,50), pos = (X_Distance + 10, Y_Distance + 270))
        self.text3 = wx.StaticText(self.panel, -1, self.t3, size = (25,50), pos = (X_Distance + 10, Y_Distance + 400))
        self.text4 = wx.StaticText(self.panel, -1, self.t4, size = (25,50), pos = (X_Distance + 315, Y_Distance + 5))
        self.text5 = wx.StaticText(self.panel, -1, self.t5, size = (0,0), pos = (X_Distance + 30, Y_Distance + 65))
        self.text6 = wx.StaticText(self.panel, -1, self.t6, size = (0,0), pos = (X_Distance + 40, Y_Distance + 95))
        self.text7 = wx.StaticText(self.panel, -1, self.t17, pos = (X_Distance + 530, Y_Distance + 98))
        self.text8 = wx.StaticText(self.panel, -1, self.t18, pos = (X_Distance + 305, Y_Distance + 138))
        self.text9 = wx.StaticText(self.panel, -1, self.t19, pos = (X_Distance + 510, Y_Distance + 138))
        self.text10 = wx.StaticText(self.panel, -1, self.t20, pos = (X_Distance + 620, Y_Distance + 138))
        self.text11 = wx.StaticText(self.panel, -1, self.t7, size = (25,1), pos = (X_Distance + 40, Y_Distance + 175))
        self.text12 = wx.StaticText(self.panel, -1, self.t8, size = (25,1), pos = (X_Distance + 40, Y_Distance + 215))
        self.text13 = wx.StaticText(self.panel, -1, self.t5, size = (0,1), pos = (X_Distance + 30, Y_Distance + 245))
        self.text14 = wx.StaticText(self.panel, -1, self.t5, size = (0,1), pos = (X_Distance + 30, Y_Distance + 295))
        self.text15 = wx.StaticText(self.panel, -1, self.t9, size = (0,1), pos = (X_Distance + 30, Y_Distance + 322))
        self.text16 = wx.StaticText(self.panel, -1, self.t10, size = (0,1), pos = (X_Distance + 435, Y_Distance + 322))
        self.text17 = wx.StaticText(self.panel, -1, self.t11, size = (0,1), pos = (X_Distance + 30, Y_Distance + 360))
        self.text18 = wx.StaticText(self.panel, -1, self.t22, size = (0,1), pos = (X_Distance + 355, Y_Distance + 322))
        self.text19 = wx.StaticText(self.panel, -1, self.t5, size = (0,1), pos = (X_Distance + 30, Y_Distance + 380))
        self.text20 = wx.StaticText(self.panel, -1, self.t12, size = (0,1), pos = (X_Distance + 30, Y_Distance + 452))
        self.text21 = wx.StaticText(self.panel, -1, self.t5, size = (0,0), pos = (X_Distance + 30, Y_Distance + 425))
        self.text22 = wx.StaticText(self.panel, -1, self.t21, size = (0,1), pos = (X_Distance + 285, Y_Distance + 452))
        self.text23 = wx.StaticText(self.panel, -1, self.t13, size = (0,1), pos = (X_Distance + 360, Y_Distance + 452))
        self.text24 = wx.StaticText(self.panel, -1, self.t22, size = (0,1), pos = (X_Distance + 565, Y_Distance + 452))
        self.text25 = wx.StaticText(self.panel, -1, self.t16, size = (0,1), pos = (X_Distance + 295, Y_Distance + 493))
        self.text26 = wx.StaticText(self.panel, -1, self.t22, size = (0,1), pos = (X_Distance + 565, Y_Distance + 493))
        self.text27 = wx.StaticText(self.panel, -1, self.t5, size = (0,0), pos = (X_Distance + 30, Y_Distance + 525))        
        self.font1 = wx.Font(19, wx.MODERN, wx.NORMAL, wx.NORMAL, False, 'Consolas') 
        self.font2 = wx.Font(15, wx.MODERN, wx.NORMAL, wx.NORMAL, False, 'Consolas')
        self.font3 = wx.Font(12, wx.MODERN, wx.NORMAL, wx.NORMAL, False, 'Consolas')
        self.text1.SetFont(self.font1)
        self.text2.SetFont(self.font1)
        self.text3.SetFont(self.font1)
        self.text4.SetFont(self.font1)
        self.text5.SetFont(self.font2)
        self.text6.SetFont(self.font2)
        self.text8.SetFont(self.font3)
        self.text9.SetFont(self.font3)
        self.text10.SetFont(self.font3)
        self.text11.SetFont(self.font2)
        self.text12.SetFont(self.font2)
        self.text13.SetFont(self.font2)
        self.text14.SetFont(self.font2)
        self.text15.SetFont(self.font3)
        self.text16.SetFont(self.font3)
        self.text17.SetFont(self.font3)
        self.text18.SetFont(self.font3)
        self.text19.SetFont(self.font2)
        self.text20.SetFont(self.font2)
        self.text21.SetFont(self.font2)
        self.text22.SetFont(self.font2)
        self.text23.SetFont(self.font2)
        self.text24.SetFont(self.font2)
        self.text25.SetFont(self.font2)
        self.text26.SetFont(self.font2)
        self.text27.SetFont(self.font2)
        self.checkbox1 = wx.CheckBox(self.panel, -1, '类别筛选', size = (70, 20), pos = (X_Distance + 180, Y_Distance + 97))
        self.checkbox2 = wx.CheckBox(self.panel, -1, '条件筛选', size = (70, 20), pos = (X_Distance + 50, Y_Distance + 138))
        self.checkbox3 = wx.CheckBox(self.panel, -1, '后缀筛选', size = (70, 20), pos = (X_Distance + 425, Y_Distance + 97))
        self.checkbox4 = wx.CheckBox(self.panel, -1, '启用备份优先级', size = (100, 20), pos = (X_Distance + 425, Y_Distance + 176))
        self.checkbox5 = wx.CheckBox(self.panel, -1, '开启多线程加速', size = (100, 20), pos = (X_Distance + 30, Y_Distance + 495))
        self.checkbox6 = wx.CheckBox(self.panel, -1, '开启内存缓冲加速', size = (120, 20), pos = (X_Distance + 165, Y_Distance + 495))
        self.List1 = ['全部文件', '记事本文件', '音频', '视频', '图片', '幻灯片', '表格',
                      '文档', '数据库文件', '注册表文件', '图标', '快捷方式']
        self.List2 = ['文件大小筛选', '文件名筛选']
        self.List3 = ['B', 'KB', 'MB', 'GB', 'TB']
        self.List4 = ['所有情况', '当文件被创建', '当文件被删除',  '当文件被修改']
        self.List5 = ['小文件优先', '大文件优先', '新文件优先', '旧文件优先']
        self.List6 = ['仅提示', '删除最早的文件', '删除最新的文件', '删除最小的文件',
                      '删除最大的文件']
        self.EntryText1 = wx.TextCtrl(self.panel, -1, size=(100, -1), pos = (X_Distance + 610, Y_Distance + 95))
        self.EntryText2 = wx.TextCtrl(self.panel, -1, size=(50, -1), pos = (X_Distance + 245, Y_Distance + 135))
        self.EntryText3 = wx.TextCtrl(self.panel, -1, size=(50, -1), pos = (X_Distance + 445, Y_Distance + 135))
        self.EntryText4 = wx.TextCtrl(self.panel, -1, size=(50, -1), pos = (X_Distance + 690, Y_Distance + 135))
        self.EntryText5 = wx.TextCtrl(self.panel, -1, size=(425, -1), pos = (X_Distance + 225, Y_Distance + 215))
        self.EntryText6 = wx.TextCtrl(self.panel, -1, size=(125, -1), pos = (X_Distance + 215, Y_Distance + 320))
        self.EntryText7 = wx.TextCtrl(self.panel, -1, size=(325, -1), pos = (X_Distance + 205, Y_Distance + 355))
        self.EntryText8 = wx.TextCtrl(self.panel, -1, size=(85, -1), pos = (X_Distance + 190, Y_Distance + 450))
        self.EntryText9 = wx.TextCtrl(self.panel, -1, size=(45, -1), pos = (X_Distance + 510, Y_Distance + 450))
        self.EntryText10 = wx.TextCtrl(self.panel, -1, size=(45, -1), pos = (X_Distance + 510, Y_Distance + 490))
        self.listbox1 = wx.Choice(self.panel, -1, size = (80, 50), pos = (X_Distance + 280, Y_Distance + 95), choices=self.List1)
        self.listbox2 = wx.Choice(self.panel, -1, size = (100, 50), pos = (X_Distance + 125, Y_Distance + 135), choices=self.List2)
        self.listbox3 = wx.Choice(self.panel, -1, size = (50, 50), pos = (X_Distance + 555, Y_Distance + 135), choices=self.List3)
        self.listbox4 = wx.Choice(self.panel, -1, size = (150, 50), pos = (X_Distance + 235, Y_Distance + 174), choices=self.List4)
        self.listbox5 = wx.Choice(self.panel, -1, size = (150, 50), pos = (X_Distance + 545, Y_Distance + 174), choices=self.List5)
        self.listbox6 = wx.Choice(self.panel, -1, size = (135, 50), pos = (X_Distance + 585, Y_Distance + 320), choices=self.List6)
        self.butten1 = wx.Button(self.panel,-1,". . .", size = (50, 25), pos = (X_Distance + 665, Y_Distance + 215))
        self.butten2 = wx.Button(self.panel,-1,". . .", size = (60, 25), pos = (X_Distance + 545, Y_Distance + 355))
        self.butten3 = wx.Button(self.panel,-1,"导出设置", size = (60, 25), pos = (X_Distance + 615, Y_Distance + 450))
        self.butten4 = wx.Button(self.panel,-1,"导入设置", size = (60, 25), pos = (X_Distance + 675, Y_Distance + 450))
        self.butten5 = wx.Button(self.panel,-1,"使用默认设置", size = (120, 25), pos = (X_Distance + 615, Y_Distance + 475))
        self.butten6 = wx.Button(self.panel,-1,"保存设置", size = (120, 25), pos = (X_Distance + 615, Y_Distance + 500))
        dialog1 = ''
        dialog2 = ''
        self.listbox1.Enable(False)
        self.listbox2.Enable(False)
        self.listbox3.Enable(False)
        self.EntryText1.Enable(False)
        self.EntryText2.Enable(False)
        self.EntryText3.Enable(False)
        self.EntryText4.Enable(False)
        self.EntryText10.Enable(False)
        self.listbox5.Enable(False)
        self.butten1.Bind(wx.EVT_BUTTON,self.OnClicked1)
        self.butten2.Bind(wx.EVT_BUTTON,self.OnClicked2)
        self.butten3.Bind(wx.EVT_BUTTON,self.OnSave)
        self.butten4.Bind(wx.EVT_BUTTON,self.OnOpen)
        self.butten5.Bind(wx.EVT_BUTTON,self.UseDefaultSettings)
        self.butten6.Bind(wx.EVT_BUTTON,self.Saved)
        threading.Timer(0.1, self.StateDetect).start()
    def UseDefaultSettings(self, event):
        self.OnOpen(1, '默认设置.txt')
    def CheckforProperty(self):
        if self.checkbox1.GetValue() == self.checkbox3.GetValue() == True:
            return '类别筛选不能与后缀筛选同时启用'
        if self.checkbox2.GetValue() == True:
            if self.listbox2.GetSelection() == 0:
                try:
                    Min = int(self.EntryText2.GetValue())
                    Max = int(self.EntryText3.GetValue())
                except ValueError:
                    return '文件大小范围只能是数字'
                else:
                    if Min >= Max:
                        return '文件大小在此范围内是空集，请重新填写'
                    if Min < 0 or Max < 0:
                        return '文件大小筛选不能为负数'
                if self.listbox3.GetSelection() == -1:
                    return '请选择文件筛选大小的单位'
        if os.path.exists(self.EntryText5.GetValue()) == os.path.exists(self.EntryText7.GetValue()) == True:
            pass
        else:
            return '选择了不存在的监视/备份存放路径'
        if self.listbox4.GetSelection() == -1:
            return '请选择备份动作触发条件'
        return True
                



        ####################
    def Saved(self, event):
        if self.CheckforProperty() == True:
            self.InitializationState = True
            self.RecordCurrentSettings()
            InFo1 = wx.MessageDialog(None,"保存成功", "消息提示")
            if InFo1.ShowModal() == wx.ID_YES:
                InFo1.Destroy()
            self.Initialization(self.EntryText5.GetValue(), self.EntryText7.GetValue(),
                                self.listbox4.GetSelection())
        else:
            InFo1 = wx.MessageDialog(None,self.CheckforProperty(), "警告")
            if InFo1.ShowModal() == wx.ID_YES:
                InFo1.Destroy() 
    def DestroySystemSettings(self, event):
        self.text1.Destroy()
        self.text2.Destroy()
        self.text3.Destroy()
        self.text4.Destroy()
        self.text5.Destroy()
        self.text6.Destroy()
        self.text7.Destroy()
        self.text8.Destroy()
        self.text9.Destroy()
        self.text10.Destroy()
        self.text11.Destroy()
        self.text12.Destroy()
        self.text13.Destroy()
        self.text14.Destroy()
        self.text15.Destroy()
        self.text16.Destroy()
        self.text17.Destroy()
        self.text18.Destroy()
        self.text19.Destroy()
        self.text20.Destroy()
        self.text21.Destroy()
        self.text22.Destroy()
        self.text23.Destroy()
        self.text24.Destroy()
        self.text25.Destroy()
        self.text26.Destroy()
        self.text27.Destroy()
        self.checkbox1.Destroy()
        self.checkbox2.Destroy()
        self.checkbox3.Destroy()
        self.checkbox4.Destroy()
        self.checkbox5.Destroy()
        self.checkbox6.Destroy()
        self.EntryText1.Destroy()
        self.EntryText2.Destroy()
        self.EntryText3.Destroy()
        self.EntryText4.Destroy()
        self.EntryText5.Destroy()
        self.EntryText6.Destroy()
        self.EntryText7.Destroy()
        self.EntryText8.Destroy()
        self.EntryText9.Destroy()
        self.EntryText10.Destroy()
        self.listbox1.Destroy()
        self.listbox2.Destroy()
        self.listbox3.Destroy()
        self.listbox4.Destroy()
        self.listbox5.Destroy()
        self.listbox6.Destroy()
        self.butten1.Destroy()
        self.butten2.Destroy()
        self.butten3.Destroy()
        self.butten4.Destroy()
        self.butten5.Destroy()
        self.butten6.Destroy()
    def StateDetect(self):
        while True:
            try:
                if self.checkbox1.GetValue() == True:
                    self.listbox1.Enable(True)
                else:
                    self.listbox1.Enable(False)
                if self.checkbox2.GetValue() == True:
                    self.listbox2.Enable(True)
                    State = False
                else:
                    self.listbox2.Enable(False)
                    State = True
                if self.checkbox3.GetValue() == True:
                    self.EntryText1.Enable(True)
                else:
                    self.EntryText1.Enable(False)
                if self.checkbox4.GetValue() == True:
                    self.listbox5.Enable(True)
                else:
                    self.listbox5.Enable(False)
                if self.checkbox6.GetValue() == True:
                    self.EntryText10.Enable(True)
                else:
                    self.EntryText10.Enable(False)
                if self.listbox2.GetSelection() == 0:
                    self.EntryText2.Enable(True)
                    self.EntryText3.Enable(True)
                    self.listbox3.Enable(True)
                    self.EntryText4.Enable(False)
                if self.listbox2.GetSelection() == 1:
                    self.EntryText2.Enable(False)
                    self.EntryText3.Enable(False)
                    self.listbox3.Enable(False)
                    self.EntryText4.Enable(True)
                if self.listbox2.GetSelection() == -1 or State == True:
                    self.EntryText2.Enable(False)
                    self.EntryText3.Enable(False)
                    self.listbox3.Enable(False)
                    self.EntryText4.Enable(False)
            except RuntimeError:
                break
            finally:
                self.listbox4.Enable(True)
                self.listbox6.Enable(True)
    def OnClicked1(self, event):
        dialog1 = wx.DirDialog(None, '监控路径选择', os.getcwd())
        if dialog1.ShowModal() == wx.ID_OK:
            target = dialog1.GetPath()
            print (target)
            dialog1.Destroy()
            self.EntryText5.SetValue(target)
    def OnClicked2(self, event):
        dialog2 = wx.DirDialog(None, '缓存文件存放路径选择', os.getcwd())
        if dialog2.ShowModal() == wx.ID_OK:
            target = dialog2.GetPath()
            print (target)
            dialog2.Destroy()
            self.EntryText7.SetValue(target)
    def OnSave(self, event):
        dialog1 = wx.FileDialog(None, '保存文件路径选择', os.getcwd(), ' 配置文件.txt', '*.txt*')
        if dialog1.ShowModal() == wx.ID_OK:
            target = dialog1.GetPath()
            behind = target[-4: -1] + target[-1]
            if behind != '.txt':
                target += '.txt'
            SaveFile = open(target, 'w')
            List = []
            CheckBoxState = ''
            List.append(self.EntryText1.GetValue())
            List.append(self.EntryText2.GetValue())
            List.append(self.EntryText3.GetValue())
            List.append(self.EntryText4.GetValue())
            List.append(self.EntryText5.GetValue())
            List.append(self.EntryText6.GetValue())
            List.append(self.EntryText7.GetValue())
            List.append(self.EntryText8.GetValue())
            List.append(self.EntryText9.GetValue())
            List.append(self.EntryText10.GetValue())
            List.append(str(self.listbox1.GetSelection()))
            List.append(str(self.listbox1.Enable()))
            List.append(str(self.listbox2.GetSelection()))
            List.append(str(self.listbox2.Enable()))
            List.append(str(self.listbox3.GetSelection()))
            List.append(str(self.listbox3.Enable()))
            List.append(str(self.listbox4.GetSelection()))
            List.append(str(self.listbox4.Enable()))
            List.append(str(self.listbox5.GetSelection()))
            List.append(str(self.listbox5.Enable()))
            List.append(str(self.listbox6.GetSelection()))
            List.append(str(self.listbox6.Enable()))
            CheckBoxState += '0' if self.checkbox1.GetValue() == False else '1'
            CheckBoxState += '0' if self.checkbox2.GetValue() == False else '1'
            CheckBoxState += '0' if self.checkbox3.GetValue() == False else '1'
            CheckBoxState += '0' if self.checkbox4.GetValue() == False else '1'
            CheckBoxState += '0' if self.checkbox5.GetValue() == False else '1'
            CheckBoxState += '0' if self.checkbox6.GetValue() == False else '1'
            List.append(CheckBoxState)
            for Element in range(len(List)):
                SaveFile.write(List[Element] + '$')
            SaveFile.close()
            print('成功保存')
            InFo1 = wx.MessageDialog(None,"导出成功", "消息提示")
            if InFo1.ShowModal() == wx.ID_YES:
                InFo1.Destroy()
    def RecordCurrentSettings(self):
        CheckBoxState = ''
        List = []
        List.append(self.EntryText1.GetValue())
        List.append(self.EntryText2.GetValue())
        List.append(self.EntryText3.GetValue())
        List.append(self.EntryText4.GetValue())
        List.append(self.EntryText5.GetValue())
        List.append(self.EntryText6.GetValue())
        List.append(self.EntryText7.GetValue())
        List.append(self.EntryText8.GetValue())
        List.append(self.EntryText9.GetValue())
        List.append(self.EntryText10.GetValue())
        List.append(str(self.listbox1.GetSelection()))
        List.append(str(self.listbox1.Enable()))
        List.append(str(self.listbox2.GetSelection()))
        List.append(str(self.listbox2.Enable()))
        List.append(str(self.listbox3.GetSelection()))
        List.append(str(self.listbox3.Enable()))
        List.append(str(self.listbox4.GetSelection()))
        List.append(str(self.listbox4.Enable()))
        List.append(str(self.listbox5.GetSelection()))
        List.append(str(self.listbox5.Enable()))
        List.append(str(self.listbox6.GetSelection()))
        List.append(str(self.listbox6.Enable()))
        CheckBoxState += '0' if self.checkbox1.GetValue() == False else '1'
        CheckBoxState += '0' if self.checkbox2.GetValue() == False else '1'
        CheckBoxState += '0' if self.checkbox3.GetValue() == False else '1'
        CheckBoxState += '0' if self.checkbox4.GetValue() == False else '1'
        CheckBoxState += '0' if self.checkbox5.GetValue() == False else '1'
        CheckBoxState += '0' if self.checkbox6.GetValue() == False else '1'
        List.append(CheckBoxState)
        self.LastSettingState.append(List)
    def BackSettings(self):
        Data1 = self.LastSettingState[-1]
        Data = Data1[0]
        self.EntryText1.SetValue(Data)
        Data = Data1[1]
        self.EntryText2.SetValue(Data)
        Data = Data1[2]
        self.EntryText3.SetValue(Data)
        Data = Data1[3]
        self.EntryText4.SetValue(Data)
        Data = Data1[4]
        self.EntryText5.SetValue(Data)
        Data = Data1[5]
        self.EntryText6.SetValue(Data)
        Data = Data1[6]
        self.EntryText7.SetValue(Data)
        Data = Data1[7]
        self.EntryText8.SetValue(Data)
        Data = Data1[8]
        self.EntryText9.SetValue(Data)
        Data = Data1[9]
        self.EntryText10.SetValue(Data)
        Data = int(Data1[10])
        self.listbox1.SetSelection(Data)
        Data = Data1[11]
        self.listbox1.Enable(self.ProcessBool(Data))
        Data = int(Data1[12])
        self.listbox2.SetSelection(Data)
        Data = Data1[13]
        self.listbox2.Enable(self.ProcessBool(Data))
        Data = int(Data1[14])
        self.listbox3.SetSelection(Data)
        Data = Data1[15]
        self.listbox3.Enable(self.ProcessBool(Data))
        Data = int(Data1[16])
        self.listbox4.SetSelection(Data)
        Data = Data1[17]
        self.listbox4.Enable(self.ProcessBool(Data))
        Data = int(Data1[18])
        self.listbox5.SetSelection(Data)
        Data = Data1[19]
        self.listbox5.Enable(self.ProcessBool(Data))
        Data = int(Data1[20])
        self.listbox6.SetSelection(Data)
        Data = Data1[21]
        self.listbox6.Enable(self.ProcessBool(Data))
        Data = Data1[22]
        State = False if Data[0] == '0' else True
        self.checkbox1.SetValue(State)
        State = False if Data[1] == '0' else True
        self.checkbox2.SetValue(State)
        State = False if Data[2] == '0' else True
        self.checkbox3.SetValue(State)
        State = False if Data[3] == '0' else True
        self.checkbox4.SetValue(State)
        State = False if Data[4] == '0' else True
        self.checkbox5.SetValue(State)
        State = False if Data[5] == '0' else True
        self.checkbox6.SetValue(State)
    def OnOpen(self, event, OpenPath = 0):
        if OpenPath == 0:
            dialog1 = wx.FileDialog(None, '载入文件路径选择', os.getcwd(), ' 配置文件.txt', '*.txt*')
            if dialog1.ShowModal() == wx.ID_OK:
                target = dialog1.GetPath()
        else:
            target = OpenPath
            f = open(target, 'r')
            Data = f.readlines()
            Data1 = Data[0].split('$')
            Data = Data1[0]
            self.EntryText1.SetValue(Data)
            Data = Data1[1]
            self.EntryText2.SetValue(Data)
            Data = Data1[2]
            self.EntryText3.SetValue(Data)
            Data = Data1[3]
            self.EntryText4.SetValue(Data)
            Data = Data1[4]
            self.EntryText5.SetValue(Data)
            Data = Data1[5]
            self.EntryText6.SetValue(Data)
            Data = Data1[6]
            self.EntryText7.SetValue(Data)
            Data = Data1[7]
            self.EntryText8.SetValue(Data)
            Data = Data1[8]
            self.EntryText9.SetValue(Data)
            Data = Data1[9]
            self.EntryText10.SetValue(Data)
            Data = int(Data1[10])
            self.listbox1.SetSelection(Data)
            Data = Data1[11]
            self.listbox1.Enable(self.ProcessBool(Data))
            Data = int(Data1[12])
            self.listbox2.SetSelection(Data)
            Data = Data1[13]
            self.listbox2.Enable(self.ProcessBool(Data))
            Data = int(Data1[14])
            self.listbox3.SetSelection(Data)
            Data = Data1[15]
            self.listbox3.Enable(self.ProcessBool(Data))
            Data = int(Data1[16])
            self.listbox4.SetSelection(Data)
            Data = Data1[17]
            self.listbox4.Enable(self.ProcessBool(Data))
            Data = int(Data1[18])
            self.listbox5.SetSelection(Data)
            Data = Data1[19]
            self.listbox5.Enable(self.ProcessBool(Data))
            Data = int(Data1[20])
            self.listbox6.SetSelection(Data)
            Data = Data1[21]
            self.listbox6.Enable(self.ProcessBool(Data))
            Data = Data1[22]
            State = False if Data[0] == '0' else True
            self.checkbox1.SetValue(State)
            State = False if Data[1] == '0' else True
            self.checkbox2.SetValue(State)
            State = False if Data[2] == '0' else True
            self.checkbox3.SetValue(State)
            State = False if Data[3] == '0' else True
            self.checkbox4.SetValue(State)
            State = False if Data[4] == '0' else True
            self.checkbox5.SetValue(State)
            State = False if Data[5] == '0' else True
            self.checkbox6.SetValue(State)
            f.close()
            InFo1 = wx.MessageDialog(None,"导入成功", "消息提示")
            if InFo1.ShowModal() == wx.ID_YES:
                InFo1.Destroy()
            print('成功载入')
    def GetChoice(self, event):
        TarGet = event.GetEventObject()
        Index = TarGet.GetSelection()
        print(Index)
        return Index
    def Process(self, Input):
        if Input == 'False':
            Output = False
        else:
            Output = True
        return Output
    def ProcessBool(self, Input):
        if Input == 'False':
            Output = False
        else:
            Output = True
        return Output 
if __name__ == '__main__':
    app = wx.App()
    frame = SystemSettings()
    frame.Center()
    frame.Show()
    app.MainLoop()
