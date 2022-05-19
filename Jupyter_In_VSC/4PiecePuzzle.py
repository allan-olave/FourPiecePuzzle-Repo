#This game was created for screen resolution of 720 * 1380
#The author completed this code using pydroid, using vivo 1811
#Some aspect that this game need to improve:
#1. the puzzle piece have unlimited move, even though its out of display
#2. The game will work only for a screen resolution of 720 * 1380
#3. etc.


import pygame, sys
from pygame.locals import *
import numpy as np
import time


BUTTONSIZE=100
SMALLBUTTON=50
Xcontrol=490
Ycontrol=1050

YELLOW=(255, 255, 0)
RED=(255, 0, 0)
BLUE=(0, 0, 255)
GREEN=(0, 255, 0)
LightGreen=(0, 180, 0)
LightRed=(0, 255, 0)##highlight
CYAN=(0, 255, 255)
PINK=(255, 100, 255)
ORANGE1=(180, 130, 0)
ORANGE2=(210, 160, 0)
ORANGE3=(240, 190, 0)
NEXTPUZZLE=(220, 220, 220)
SUBMIT=(215, 215, 215)
FLIP=(255, 255, 255)
NEWGAME=(218, 218, 218)
borderColor=(200, 0, 70)
winColor= (0, 130, 180)
xMarkColor=(255, 255, 0)
ctrPntColor=(0, 0, 0)
txt_color=(0, 0, 0)
btnsDrawingColor=(0, 0, 0)
patternColor=(0, 255, 0)
borderPatternColor=(240, 0, 0)
solvedPuzzleColor1=(0, 255, 0)
solvedPuzzleColor2=(0, 255, 0)
borderSolvedPuzzleColor=(240, 0, 0)
puzzleWidth=169
timeLimit=200


YELLOWRECT=pygame.Rect(Xcontrol, Ycontrol, BUTTONSIZE, BUTTONSIZE)
BLUERECT=pygame.Rect(Xcontrol-100, Ycontrol+100, BUTTONSIZE, BUTTONSIZE)
REDRECT=pygame.Rect(Xcontrol+100, Ycontrol+100, BUTTONSIZE, BUTTONSIZE)
GREENRECT=pygame.Rect(Xcontrol, Ycontrol+200, BUTTONSIZE, BUTTONSIZE)
CYANRECT=pygame.Rect(25, 1050, BUTTONSIZE, BUTTONSIZE)
PINKRECT=pygame.Rect(150, 1050, BUTTONSIZE, BUTTONSIZE)
ORANGE1RECT=pygame.Rect(125, 1175, SMALLBUTTON, SMALLBUTTON)
ORANGE2RECT=pygame.Rect(210, 1175, SMALLBUTTON, SMALLBUTTON)
ORANGE3RECT=pygame.Rect(295, 1175, SMALLBUTTON, SMALLBUTTON)
FLIPRECT=pygame.Rect(Xcontrol, Ycontrol+100, BUTTONSIZE, BUTTONSIZE)
NEXTPUZZLERECT=pygame.Rect(280, 1050, 190, 90)
SUBMITRECT=pygame.Rect(280, 1267, 190, 100)
NEWGAMERECT=pygame.Rect(25, 1267, 190, 100)



win_bg_color=(0, 255, 0)
winx=720
winy=1380
win=pygame.display.set_mode((winx, winy))
FPS=30



class checkMethods:
	def isXWithinRange(self, x, xcoor1, xcoor2):
		if x>=xcoor1 and x<xcoor2:
			return 'ax'
		elif x<=xcoor1 and x>xcoor2:
			return 'bx'
		else:
			return 'x'
	
	def isYWithinRange(self, y, ycoor1, ycoor2):
		if y<=ycoor1 and y>ycoor2:
			return 'ay'
		elif y>=ycoor1 and y<ycoor2:
			return 'by'
		else:
			return 'y'

	def genNumOffset(self, polCoorList, width):
		def xCoor(polCoorList):
			for x in range(len(polCoorList)):
				xNum=polCoorList[x][0]
				yield xNum
		def yCoor(polCoorList):
			for y in range(len(polCoorList)):
				yNum=polCoorList[y][1]
				yield yNum
		xMin=min(xCoor(polCoorList))
		xMax=max(xCoor(polCoorList))
		yMin=min(yCoor(polCoorList))
		yMax=max(yCoor(polCoorList))
		numVerLineTemp=round(xMax-xMin)//width
		numHorLineTemp=round(yMax-yMin)//width
		if ((xMax-xMin)%width)!=0:
			numVerLine=int(round(numVerLineTemp))
		else:
			numVerLine=int(round(numVerLineTemp)-1)
		if ((yMax-yMin)%width)!=0:
			numHorLine=int(round(numHorLineTemp))
		else:
			numHorLine=int(round(numHorLineTemp)-1)
		def numVer(numVerLine):
			for i in range(1, numVerLine+1):
				newX=xMin+(width*i)
				yield newX
		def numHor(numHorLine):
			for j in range(1, numHorLine+1):
				newY=yMin+(width*j)
				yield newY
		verCoor=tuple(numVer(numVerLine))
		horCoor=tuple(numHor(numHorLine))
		return verCoor, horCoor

	def genPtIntersect(self, polCoorList, width):
		verXlist, horYlist=self.genNumOffset(polCoorList, width)
		def polCoorListMod(polCoorList):
			addxy=polCoorList[0]
			for coor in polCoorList:
				yield coor
				if coor==polCoorList[len(polCoorList)-1]:
					yield addxy
		polCoorMod=tuple(polCoorListMod(polCoorList))
		def verCoor(verXlist, polCoorMod):
			for i in range(len(polCoorMod)-1):
				x1, y1=polCoorMod[i]
				x2, y2=polCoorMod[i+1]
				angle1=self.getAngle(x2, y2, x1, y1)
				angle=self.validAngle(0, angle1)
				for j in range(len(verXlist)):
					xCategory=self.isXWithinRange(verXlist[j], x1, x2)
					if angle!=90 or angle!=270:
						m=round((np.tan(np.radians(angle))),4)
						if xCategory=='ax':
							y=round(y2-(m*(x2-verXlist[j])))
							withinXrange=True
						elif xCategory=='bx':
							y=round(y1-(m*(x1-verXlist[j])))
							withinXrange=True
						else:
							withinXrange=False
						if withinXrange:
							yield (verXlist[j], y)
							withinXrange=False
		def horCoor(horYlist, polCoorMod):
			for i in range(len(polCoorMod)-1):
				x1, y1=polCoorMod[i]
				x2, y2=polCoorMod[i+1]
				angle1=self.getAngle(x2, y2, x1, y1)
				angle=self.validAngle(0, angle1)
				for k in range(len(horYlist)):
					yCategory=self.isYWithinRange(horYlist[k], y1, y2)
					if angle!=90 or angle!=270:
						m=round((np.tan(np.radians(angle))),4)
						if yCategory=='ay':
							x=round((x1-((y1-horYlist[k])/m)))
							withinYrange=True
						elif yCategory=='by':
							x=round((x2-((y2-horYlist[k])/m)))
							withinYrange=True
						else:
							withinYrange=False
						if withinYrange:
							yield (x, horYlist[k])
							withinYrange=False
					else:
						if yCategory=='ay' or yCategory=='by':
							x=x1
							yield (x, horYlist[k])
		verCoorMod=tuple(verCoor(verXlist, polCoorMod))
		horCoorMod=tuple(horCoor(horYlist, polCoorMod))
		def verCoorList(verXlist, verCoorMod):
			for k in verXlist:
				pairCoor=[]
				for l,m in enumerate(verCoorMod):
					if k==m[0]:
						if m not in pairCoor:
							pairCoor.append(m)
				pairCoor.sort()
				num=len(pairCoor)
				if num%2==0 and num!=0:
					for n in range(0, num, 2):
						xy2=(pairCoor[n], pairCoor[n+1])
						yield xy2
				elif num==3:
					del pairCoor[1]
					xy2=(pairCoor[0], pairCoor[1])
					yield xy2
		def horCoorList(horYlist, horCoorMod):
			for p in horYlist:
				pairCoor2=[]
				for q,r in enumerate(horCoorMod):
					if p==r[1]:
						if r not in pairCoor2:
							pairCoor2.append(r)
				pairCoor2.sort()
				num2=len(pairCoor2)
				if num2%2==0 and num2!=0:
					for n in range(0, num2, 2):
						yx2=(pairCoor2[n], pairCoor2[n+1])
						yield yx2
				elif num2==3:
					del pairCoor2[1]
					yx2=(pairCoor2[0], pairCoor2[1])
					yield yx2
		verCoorListMod=tuple(verCoorList(verXlist, verCoorMod))
		horCoorListMod=tuple(horCoorList(horYlist, horCoorMod))
		return verCoorListMod, horCoorListMod

	def combinedCoor(self, p1, p2):
		unite=p1,p2
		for x, y in enumerate(unite):
			if y!=0:
				for i in y:
					yield i
	
	def genGridPoints(self, polCoorList, width, puzzlePattern):
		coorVerPnt, coorHorPnt=self.genPtIntersect(polCoorList, width)
		def gridPoints(polCoorList, coorVerPnt, coorHorPnt, width):
			for i in coorVerPnt:
				if i!=[]:
					verPnt1, verPnt2=i
					verPnt1=list(verPnt1)
					verPnt2=list(verPnt2)
					for j in coorHorPnt:
						if j!=[]:
							horPnt1, horPnt2=j
							horPnt1=list(horPnt1)
							horPnt2=list(horPnt2)
							if verPnt1[1]>verPnt2[1]:
								verPnt1[1], verPnt2[1]=verPnt2[1], verPnt1[1]
							if horPnt1[1]>=verPnt1[1] and horPnt1[1]<=verPnt2[1]:
								yield (verPnt1[0], horPnt1[1])
			for k in coorHorPnt:
				if k!=[]:
					horPnt3, horPnt4=k
					horPnt3=list(horPnt3)
					horPnt4=list(horPnt4)
					for l in coorVerPnt:
						if l!=[]:
							verPnt3, verPnt4=l
							verPnt3=list(verPnt3)
							verPnt4=list(verPnt4)
							if horPnt3[0]>horPnt4[0]:
								horPnt3[0], horPnt4[0]=horPnt4[0], horPnt4[0]
							if verPnt3[0]<=horPnt3[0] and verPnt3[0]>=horPnt4[0]:
								yield (verPnt3[0], horPnt3[1])
#####adding horizontal and vertical line coordinates:
		gridPnts=tuple(gridPoints(polCoorList, coorVerPnt, coorHorPnt, width))
		if puzzlePattern:
			additionCoor=tuple(self.pntsAlongBorder(coorVerPnt, coorHorPnt))
			gridPnts=tuple(self.combinedCoor(gridPnts, additionCoor))
		return gridPnts
			
	def pntsAlongBorder(self, coorVerPnt, coorHorPnt):
		for i in coorVerPnt:
			x, y=i
			yield x
			yield y
		for j in coorHorPnt:
			x1, y1=j
			yield x1
			yield y1
	
	def isPuzzlePieceOvrLap(self, piece1, piece2, piece3, piece4, width):
		def genPieceGridPnts(p1, p2, p3, p4, width):
			pieces=p1, p2, p3, p4
			for i in pieces:
				Pnts=self.genGridPoints(i, width, False)
				yield Pnts
		pieceGridPnts=tuple(genPieceGridPnts(piece1, piece2, piece3, piece4, width))
		for j, k in enumerate(pieceGridPnts):
			if j!=len(pieceGridPnts)-1:
				for l in k:
					m, n=l
					square=pygame.Rect(m-5, n-5, 10, 10)
					for o, p in enumerate(pieceGridPnts):
						if o!=j and o>j:
							for q in p:
								if square.collidepoint(q):
									pygame.draw.circle(self.win, (0, 0, 220), q, 10)
									return True
		return False
	
	def isWithinPolygon(self, piece1, piece2, piece3, piece4, polCoorList, width):
		puzzleCoorList=list(piece4)+list(piece3)+list(piece2)+list(piece1)
		gridPoints=self.genGridPoints(polCoorList, width, True)
		Pnts=self.combinedCoor(polCoorList, gridPoints)
		for h, i in enumerate(Pnts):
			j, k=i
			square=pygame.Rect(j-20, k-20, 40, 40)
			if h<len(polCoorList):
				withinSquare=False
				for m,n in enumerate(puzzleCoorList):
					if square.collidepoint(n) or m<(len(puzzleCoorList)-1):
						if square.collidepoint(n):
							withinSquare=True
							puzzleCoorList.remove(n)
					else:
						if not withinSquare:
							return False

			else:
				if puzzleCoorList!=[]:
					for o in puzzleCoorList:
						if square.collidepoint(o):
							puzzleCoorList.remove(o)
				else:
					return True
		if puzzleCoorList==[]:
			return True
		else:
			return False

class flipMethods(checkMethods):
	def flipCoordinates(self, coorList):
		if len(coorList)!=6: 
			xMidPnt=round(((coorList[0][0]+ coorList[1][0])/2), 4)
			yMidPnt=round(((coorList[0][1]+coorList[1][1])/2), 4)
			angle1=self.getAngle(coorList[0][0], coorList[0][1], coorList[1][0], coorList[1][1])
		elif self.i==3 or len(coorList)==6:
			xMidPnt=round(((coorList[0][0]+ coorList[4][0])/2), 4)
			yMidPnt=round(((coorList[0][1]+coorList[4][1])/2), 4)
			angle1=self.getAngle(coorList[0][0], coorList[0][1], coorList[4][0], coorList[4][1])
		angle=self.validAngle(0, angle1)
		for i in range(len(coorList)):
			xPnt=coorList[i][0]
			yPnt=coorList[i][1]
			if angle==90 or angle==270:
				flip=self.flipRefEqnHorizontal(yMidPnt, xPnt, yPnt)
				yield flip
			elif angle==0 or angle==180:
				flip=self.flipRefEqnVertical(xMidPnt, xPnt, yPnt)
				yield flip
			else:
				m=round((np.tan(np.radians(angle))),4)
				mPerpen=round((-1/m),4)
				flip=self.flipSlopeTilted(xMidPnt, yMidPnt, xPnt, yPnt, m, mPerpen)
				yield flip	
		
	def flipRefEqnVertical(self, xMidpnt, xPnt, yPnt):
		if xMidpnt<xPnt:
			xNew=xMidpnt-(xPnt-xMidpnt)
		elif xMidpnt>xPnt:
			xNew=xMidpnt+(xMidpnt-xPnt)
		else:
			xNew=xPnt
		return xNew, yPnt
	
	def flipRefEqnHorizontal(self, yMidpnt, xPnt, yPnt):
		if yMidpnt<yPnt:
			yNew=yMidpnt-(yPnt-yMidpnt)
		elif yMidpnt>yPnt:
			yNew=yMidpnt+(yMidpnt-yPnt)
		else:
			yNew=yPnt
		return xPnt, yNew
		
	def flipSlopeTilted(self, xMidpnt, yMidpnt, xPnt, yPnt, m, mPerpen):
		xRef=round(((((mPerpen*xMidpnt)-yMidpnt)-((m*xPnt)-yPnt))/(mPerpen-m)), 4)
		yRef=round(((mPerpen*(xRef-xMidpnt))+yMidpnt),4)
		if xPnt>xRef and yPnt<yRef:
			xNew=xRef-(xPnt-xRef)
			yNew=yRef+(yRef-yPnt)
		elif xPnt<xRef and yPnt>yRef:
			xNew=xRef+(xRef-xPnt)
			yNew=yRef-(yPnt-yRef)
		elif xPnt<xRef and yPnt<yRef:
			xNew=xRef+(xRef-xPnt)
			yNew=yRef+(yRef-yPnt)
		elif xPnt>xRef and yPnt>yRef:
			xNew=xRef-(xPnt-xRef)
			yNew=yRef-(yPnt-yRef)
		else:
			xNew=xPnt
			yNew=yPnt
		return xNew, yNew

class rotationMethods(flipMethods):
	def genNumRotated(self, listNum, xVar, yVar, slope, xcntr, ycntr):
		xcenter, ycenter=xcntr+xVar, ycntr+yVar
		cntr=(xcenter, ycenter)
		for j,i in enumerate(listNum):
			x, y=i
			xcoor=x+xVar
			ycoor=y+yVar
			d=round(((ycoor-ycenter)**2+(xcoor-xcenter)**2)**0.5, 4)
			angle1=self.getAngle(xcoor, ycoor, xcenter, ycenter)
			angle=self.validAngle(slope, angle1)
			xNew=round(((d*np.cos(np.radians(angle)))+xcenter), 4)
			yNew=round(((d*np.sin(np.radians(angle)))+ycenter), 4)
			num=(xNew, yNew)
			yield num
			if j==len(listNum)-1:
				yield cntr

	def getAngle(self, xcoor, ycoor, xcenter, ycenter):
		if (xcoor-xcenter)!=0:
			angle1=round(np.degrees(np.arctan((ycoor-ycenter)/(xcoor-xcenter))), 4)
			if xcoor>xcenter and ycoor>ycenter:
				angle=angle1
			elif xcoor<xcenter and (ycoor>ycenter or ycoor<ycenter):
				angle=180+angle1
			elif xcoor>xcenter and ycoor<ycenter:
				angle=360+angle1
			elif xcoor>xcenter and ycoor==ycenter:
				angle=0
			elif xcoor<xcenter and ycoor==ycenter:
				angle=180
		else:
			if ycoor>ycenter:
				angle=90
			elif ycoor<ycenter:
				angle=270
			else:
				angle=0
		return angle

	def validAngle(self, slope, angle2):		
		sumAngle=(slope+angle2)%360
		return sumAngle


class Tiles(rotationMethods):
	def __init__(self, borderColor, winColor, xMarkColor, ctrPntColor, txt_color, btnsDrawingColor, patternColor, borderPatternColor, solvedPuzzleColor1, solvedPuzzleColor2, borderSolvedPuzzleColor, timeLimit, win_bg_color, LightGreen, LightRed, win, puzzleWidth):
		self.borderColor=borderColor
		self.winColor=winColor
		self.xMarkColor=xMarkColor
		self.ctrPntColor=ctrPntColor
		self.txt_color=txt_color
		self.btnsDrawingColor=btnsDrawingColor
		self.patternColor=patternColor
		self.borderPatternColor=borderPatternColor
		self.solvedPuzzleColor1=solvedPuzzleColor1
		self.solvedPuzzleColor2=solvedPuzzleColor2
		self.borderSolvedPuzzleColor=borderSolvedPuzzleColor
		self.timeLimit=timeLimit
		self.win_bg_color=win_bg_color
		self.win=win
		self.puzzleWidth=puzzleWidth
		self.flipCoor=False
		self.permit=True
		self.gameOver=False
		self.i=self.j=0
		self.xcntr1, self.ycntr1=81, 91
		self.xcntr2, self.ycntr2=256, 67
		self.xcntr3, self.ycntr3=95, 450
		self.xcntr4, self.ycntr4=284, 484
		self.colorList=((LightRed, LightGreen, LightGreen, LightGreen), (LightGreen, LightRed, LightGreen, LightGreen), (LightGreen, LightGreen, LightRed, LightGreen), (LightGreen, LightGreen, LightGreen, LightRed))
		self.speedColor=((LightRed, ORANGE1, ORANGE1,), (ORANGE2, LightRed, ORANGE2), (ORANGE3, ORANGE3, LightRed))
		self.countTimer=self.timeLimit
		self.clock=[]
		self.numPuzzle=0
		self.speedList=(0.5, 7, 30)
		self.flipStatus=[0, 0, 0, 0]
		self.parameter=[[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]
		self.myList1=((10, 10), (179, 10), (179, 80.0021), (10, 249.0021))
		self.myList2=((199, 10), (368, 10), (199, 179))
		self.myList3=((10, 269), (179, 269), (179, 578.0042), (10, 747.0042))
		self.myList4=((199, 269), (318.5011, 388.5011), (368.0001, 339.0022), (368.0001, 578.0043), (199, 747.0043))
		self.puzzleList=[((620, 21), (667, 21), (667, 154), (573, 248), (573, 115), (620, 115)), ((620, 20), (671, 143), (620, 266), (569, 143)), ((554, 53), (601, 53), (601, 186), (687, 186), (687, 233), (554, 233)), ((573, 110), (667, 16), (667, 82), (639, 110), (639, 176), (667, 204), (667, 270), (573, 176)), ((541, 112), (620, 79), (700, 112), (682, 155), (664, 163), (682, 206), (620, 181), (559, 206), (577, 163), (559, 155)), ((530.0, 142.5), (577.0, 95.5), (663.0, 95.5), (710.0, 142.5), (682.0, 142.5), (682.0, 189.5), (549.0, 189.5), (549.0, 142.5)), ((526.0, 182.0), (573.0, 135.0), (573.0, 69.0), (606.0, 102.0), (620.0, 88.0), (634.0, 102.0), (667.0, 69.0), (667.0, 135.0), (714.0, 182.0), (681.0, 216.0), (620.0, 155.0), (559.0, 216.0)),((544.0, 142.5), (563.0, 142.5), (563.0, 95.5), (696.0, 95.5), (696.0, 142.5), (677.0, 142.5), (677.0, 189.5), (544.0, 189.5)), ((526.0, 62.5), (620.0, 156.5), (714.0, 62.5), (714.0, 128.5), (620.0, 222.5), (526.0, 128.5)), ((569.0, 143.0), (602.0, 63.0), (663.0, 38.0), (645.0, 81.0), (671.0, 143.0), (645.0, 204.0), (663.0, 247.0), (602.0, 222.0)), ((526.0, 170.0), (620.0, 76.0), (714.0, 170.0), (667.0, 170.0), (667.0, 209.0), (573.0, 209.0), (573.0, 170.0)), ((573.0, 66.5), (606.0, 99.5), (620.0, 85.5), (634.0, 99.5), (667.0, 66.5), (667.0, 218.5), (573.0, 218.5)), ((573.0, 85.5), (587.0, 99.5), (620.0, 66.5), (653.0, 99.5), (667.0, 85.5), (667.0, 218.5), (573.0, 218.5)), ((553.5, 76.0), (600.5, 76.0), (600.5, 115.0), (647.5, 115.0), (647.5, 162.0), (686.5, 162.0), (686.5, 209.0), (553.5, 209.0)), ((553.5, 52.5), (686.5, 52.5), (686.5, 99.5), (647.5, 99.5), (647.5, 232.5), (600.5, 232.5), (600.5, 99.5), (553.5, 99.5)), ((573.0, 99.5), (620.0, 52.5), (667.0, 99.5), (667.0, 232.5), (620.0, 185.5), (573.0, 232.5)), ((540.5, 163.0), (558.5, 155.0), (576.5, 112.0), (558.5, 104.0), (619.5, 79.0), (681.5, 104.0), (663.5, 112.0), (681.5, 155.0), (699.5, 163.0), (681.5, 206.0), (619.5, 181.0), (558.5, 206.0)), ((530.0, 95.5), (549.0, 95.5), (549.0, 48.5), (596.0, 95.5), (663.0, 95.5), (663.0, 142.5), (710.0, 189.5), (690.0, 189.5), (690.0, 236.5), (643.0, 189.5), (577.0, 189.5), (577.0, 142.5)), ((526.0, 95.0), (573.0, 95.0), (573.0, 76.0), (620.0, 123.0), (667.0, 76.0), (667.0, 95.0), (714.0, 95.0), (667.0, 142.0), (667.0, 209.0), (573.0, 209.0), (573.0, 142.0)), ((556.5, 73.5), (589.5, 106.5), (617.5, 79.5), (650.5, 112.5), (683.5, 79.5), (683.5, 211.5), (650.5, 178.5), (622.5, 206.5), (589.5, 173.5), (556.5, 206.5)), ((530.0, 162.0), (549.0, 162.0), (549.0, 115.0), (596.0, 162.0), (596.0, 76.0), (643.0, 76.0), (643.0, 162.0), (690.0, 115.0), (690.0, 162.0), (710.0, 162.0), (663.0, 209.0), (577.0, 209.0)), ((493.0, 180.0), (587.0, 86.0), (587.0, 152.0), (626.0, 152.0), (626.0, 86.0), (720.0, 180.0), (673.0, 180.0), (673.0, 199.0), (540.0, 199.0), (540.0, 180.0))]
		self.submit=False
		self.solvedPuzzle={}
		self.gamePlayedTime=[]

	def convertPuzzleList(self, puzzle):
		for i in puzzle:
			x, y=i
			convrt=round((x-520)*(720/200), 5), round(y*(720/200), 5)
			yield convrt

	def drawCircle(self, ctr1, ctr2, ctr3, ctr4):
		pygame.draw.circle(self.win, self.ctrPntColor, ctr1, 10)
		pygame.draw.circle(self.win, self.ctrPntColor, ctr2, 10)
		pygame.draw.circle(self.win, self.ctrPntColor, ctr3, 10)
		pygame.draw.circle(self.win, self.ctrPntColor, ctr4, 10)
		
	
	
	def genNumList(self, listNum, xVar, yVar, slope, xcntr, ycntr, pol):
		numRotatedList=self.genNumRotated(listNum, xVar, yVar, slope, xcntr, ycntr)
		numRotatedList=tuple(numRotatedList)
		if self.flipStatus[pol]%2==1:
			flipCoorList=self.flipCoordinates(numRotatedList)
			flipCoorList=tuple(flipCoorList)
			numPolList=tuple(y for y in flipCoorList if y!=flipCoorList[len(flipCoorList)-1])
			cntrCoor=flipCoorList[len(flipCoorList)-1]
			return numPolList, cntrCoor
		numPolList=tuple(x for x in numRotatedList if x!=numRotatedList[len(numRotatedList)-1])
		cntrCoor=numRotatedList[len(numRotatedList)-1]
		return numPolList, cntrCoor
	
	def countDownTimer(self):
		x=time.time()
		if self.clock==[]:
			self.clock.append(x)
		if round((x-self.clock[0]), 1)==1:
			self.countTimer-=1
			self.clock=[]
		elif round((x-self.clock[0]), 1)==2:
			self.countTimer-=2
			self.clock=[]
		if self.countTimer==0 or self.countTimer==-1:
			self.parameter=[[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]
			self.flipStatus=[0, 0, 0, 0]
			self.countTimer=self.timeLimit
			self.numPuzzle+=1
			self.gamePlayedTime.append('Not Solved')
			if self.numPuzzle==(len(self.puzzleList)):
				self.numPuzzle=0
				self.gameOver=True
			
	def drawGameOver(self):
		self.makeText(50, 'GAME FINISHED', (160, 90))
		self.makeText(35, 'Game Summary:', (30, 170))
		for i, j in enumerate(self.gamePlayedTime):
			k=1+i
			num=(len(self.puzzleList)//2+(len(self.puzzleList)%2))
			if i>=num:
				l=i%num
				if j=='Not Solved':
					self.makeText(30, f'Puzzle {k}: {j}', (360, (l*50)+230))
				else:
					self.makeText(30, f'Puzzle {k}: {j} secs', (360, (l*50)+230))
			else:
				if j=='Not Solved':
					self.makeText(30, f'Puzzle {k}: {j}', (30, (i*50)+230))
				else:
					self.makeText(30, f'Puzzle {k}: {j} secs', (30, (i*50)+230))

	def draw_board(self):
		self.win.fill(self.winColor)
		if self.gameOver:
			self.drawGameOver()
		else:
			if self.numPuzzle not in self.solvedPuzzle:
				self.playPuzzle()
				self.countDownTimer()
			else:
				self.drawSolvedPuzzle()
		self.move()
		self.drawButtons()
		
	def drawSolvedPuzzle(self):
		pygame.draw.polygon(self.win, self.solvedPuzzleColor1, self.solvedPuzzle[self.numPuzzle])
		pygame.draw.polygon(self.win, self.borderSolvedPuzzleColor, self.solvedPuzzle[self.numPuzzle], 7)
		pygame.draw.polygon(self.win, self.solvedPuzzleColor2, self.puzzleList[self.numPuzzle])
		pygame.draw.polygon(self.win, self.borderSolvedPuzzleColor, self.puzzleList[self.numPuzzle], 4)
	
	def playPuzzle(self):
		Pol1, cntr1=self.genNumList(self.myList1, self.parameter[0][1], self.parameter[0][2], self.parameter[0][0], self.xcntr1, self.ycntr1, 0)
		cntrX1, cntrY1=cntr1
		self.pieceRect1=pygame.Rect(cntrX1-50, cntrY1-50, 100, 100)
		Pol2, cntr2=self.genNumList(self.myList2, self.parameter[1][1], self.parameter[1][2], self.parameter[1][0], self.xcntr2, self.ycntr2, 1)
		cntrX2, cntrY2=cntr2
		self.pieceRect2=pygame.Rect(cntrX2-50, cntrY2-50, 100, 100)
		Pol3, cntr3=self.genNumList(self.myList3, self.parameter[2][1], self.parameter[2][2], self.parameter[2][0], self.xcntr3, self.ycntr3, 2)
		cntrX3, cntrY3=cntr3
		self.pieceRect3=pygame.Rect(cntrX3-50, cntrY3-50, 100, 100)
		Pol4, cntr4=self.genNumList(self.myList4, self.parameter[3][1], self.parameter[3][2], self.parameter[3][0], self.xcntr4, self.ycntr4, 3)
		cntrX4, cntrY4=cntr4
		self.pieceRect4=pygame.Rect(cntrX4-50, cntrY4-50, 100, 100)
		self.drawPiece(Pol1, Pol2, Pol3, Pol4)
		self.drawCircle(cntr1, cntr2, cntr3, cntr4)
		self.drawPattern(Pol1, Pol2, Pol3, Pol4)
	
	def drawPattern(self, Pol1, Pol2, Pol3, Pol4):
		pygame.draw.polygon(self.win, self.patternColor, self.puzzleList[self.numPuzzle])
		pygame.draw.polygon(self.win, self.borderPatternColor, self.puzzleList[self.numPuzzle], 4)
		convrted=tuple(self.convertPuzzleList(self.puzzleList[self.numPuzzle]))
		if self.submit:
			if self.isWithinPolygon(Pol1, Pol2, Pol3, Pol4, convrted, 20):
				if not self.isPuzzlePieceOvrLap(Pol1, Pol2, Pol3, Pol4, 10):
					if self.numPuzzle not in self.solvedPuzzle:
						self.solvedPuzzle[self.numPuzzle]=convrted
						taym=self.timeLimit-self.countTimer
						self.gamePlayedTime.append(taym)
		self.submit=False
		self.drawCursor(convrted)

	def touchPiece(self, mousex, mousey):
		if self.pieceRect1.collidepoint((mousex, mousey)):
			self.i=0
		elif self.pieceRect2.collidepoint((mousex, mousey)):
			self.i=1
		elif self.pieceRect3.collidepoint((mousex, mousey)):
			self.i=2
		elif self.pieceRect4.collidepoint((mousex, mousey)):
			self.i=3
	
	def touchSpeed(self, clickedButton):
		if clickedButton==ORANGE1:
			self.j=0
		elif clickedButton==ORANGE2:
			self.j=1
		elif clickedButton==ORANGE3:
			self.j=2
	
	def touchControls(self, clickedButton):
		if clickedButton==BLUE:
			self.parameter[self.i][1]-=self.speedList[self.j]
		elif clickedButton==RED:
			self.parameter[self.i][1]+=self.speedList[self.j]
		elif clickedButton==YELLOW:
			self.parameter[self.i][2]-=self.speedList[self.j]
		elif clickedButton==GREEN:
			self.parameter[self.i][2]+=self.speedList[self.j]
		elif clickedButton==PINK:
			self.parameter[self.i][0]+=self.speedList[self.j]
		elif clickedButton==CYAN:
			self.parameter[self.i][0]-=self.speedList[self.j]
		elif clickedButton==FLIP:	
			if (self.flipStatus[self.i]%2)==0:
				self.flipCoor=True
			else:
				self.flipCoor=False
			self.flipStatus[self.i]+=1
		elif clickedButton==SUBMIT:
			self.submit=True

	def move(self):
		clickedButton=None
		mousex, mousey=None, None
		for event in pygame.event.get():
			if event.type==pygame.QUIT:
				self.checkForQuit()
			if event.type==pygame.MOUSEBUTTONDOWN:
				mousex, mousey=event.pos
				clickedButton = self.getButtonClicked(mousex, mousey)
				if self.numPuzzle not in self.solvedPuzzle:
					self.touchPiece(mousex, mousey)
					self.touchSpeed(clickedButton)
					self.touchControls(clickedButton)
				if clickedButton==NEXTPUZZLE:
					if self.numPuzzle==len(self.gamePlayedTime):
						self.gamePlayedTime.append('Not Solved')
					self.parameter=[[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]
					self.flipStatus=[0, 0, 0, 0]
					self.numPuzzle+=1
					self.countTimer=self.timeLimit
					self.clock=[]
					if self.numPuzzle==(len(self.puzzleList)):
						self.numPuzzle=0
						self.gameOver=True
				elif clickedButton==NEWGAME:
					self.gameOver=False
					self.clock=[]
					self.solvedPuzzle={}
					self.parameter=[[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]
					self.numPuzzle=0
					self.flipStatus=[0, 0, 0, 0]
					self.i=self.j=0
					self.countTimer=self.timeLimit
	
	def getButtonClicked(self, x, y):
		if YELLOWRECT.collidepoint((x, y)):
			return YELLOW
		elif BLUERECT.collidepoint((x, y)):
			return BLUE
		elif REDRECT.collidepoint((x, y)):
			return RED
		elif GREENRECT.collidepoint((x, y)):
			return GREEN
		elif CYANRECT.collidepoint((x, y)):
			return CYAN
		elif PINKRECT.collidepoint((x, y)):
			return PINK
		elif ORANGE1RECT.collidepoint((x, y)):
			return ORANGE1
		elif ORANGE2RECT.collidepoint((x, y)):
			return ORANGE2
		elif ORANGE3RECT.collidepoint((x, y)):
			return ORANGE3
		elif FLIPRECT.collidepoint((x, y)):
			return FLIP
		elif NEXTPUZZLERECT.collidepoint((x, y)):
			return NEXTPUZZLE
		elif NEWGAMERECT.collidepoint((x, y)):
			return NEWGAME
		elif SUBMITRECT.collidepoint((x, y)):
			return SUBMIT
	
	def drawPiece(self, piece1, piece2, piece3, piece4):
		pygame.draw.polygon(self.win, self.colorList[0][self.i], piece1)
		pygame.draw.polygon(self.win, self.borderColor, piece1, 8)
		pygame.draw.polygon(self.win, self.colorList[1][self.i], piece2)
		pygame.draw.polygon(self.win, self.borderColor, piece2, 8)
		pygame.draw.polygon(self.win, self.colorList[2][self.i], piece3)
		pygame.draw.polygon(self.win, self.borderColor, piece3, 8)
		pygame.draw.polygon(self.win, self.colorList[3][self.i], piece4)
		pygame.draw.polygon(self.win, self.borderColor, piece4, 8)
			
	def drawButtons(self):
		pygame.draw.rect(self.win, YELLOW, YELLOWRECT)
		pygame.draw.rect(self.win, BLUE, BLUERECT)
		pygame.draw.rect(self.win, RED, REDRECT)
		pygame.draw.rect(self.win, GREEN, GREENRECT)
		pygame.draw.rect(self.win, CYAN, CYANRECT)
		pygame.draw.rect(self.win, PINK, PINKRECT)
		pygame.draw.rect(self.win, self.speedColor[0][self.j], ORANGE1RECT)
		pygame.draw.rect(self.win, self.speedColor[1][self.j], ORANGE2RECT)
		pygame.draw.rect(self.win, self.speedColor[2][self.j], ORANGE3RECT)
		pygame.draw.rect(self.win, NEXTPUZZLE, NEXTPUZZLERECT)
		pygame.draw.rect(self.win, NEWGAME, NEWGAMERECT)
		pygame.draw.rect(self.win, SUBMIT, SUBMITRECT)
		pygame.draw.circle(self.win, self.btnsDrawingColor, (200, 1100), 40, 4)
		pygame.draw.circle(self.win, self.btnsDrawingColor, (75, 1100), 40, 4)
		pygame.draw.polygon(self.win, self.btnsDrawingColor, ((113, 1100), (93, 1115), (120, 1123)))
		pygame.draw.polygon(self.win, self.btnsDrawingColor, ((225, 1100), (248, 1105), (232, 1123)))
		self.makeText(30, 'Next Puzzle', (287, 1085))
		self.makeText(30, 'New Game', (40, 1302))
		self.makeText(30, 'Submit', (327, 1302))
		self.makeText(30, 'FLIP', (510, 1185))
		self.makeText(30, 'Speed    1        2         3', (20, 1185))
		if not self.gameOver:
			self.makeText(30, f'TIME: {self.countTimer}', (10, 10))
			self.makeText(30, 'PATTERN', (560, 295))
		###UP arrow
		pygame.draw.line(self.win, self.btnsDrawingColor, (540, 1080), (540, 1125), 20)
		pygame.draw.polygon(self.win, self.btnsDrawingColor, ((540, 1065), (510, 1095), (570, 1095)))
		###DOWN arrow
		pygame.draw.line(self.win, self.btnsDrawingColor, (540, 1275), (540, 1315), 20)
		pygame.draw.polygon(self.win, self.btnsDrawingColor, ((540, 1335), (510, 1305), (570, 1305)))
		###LEFT arrow
		pygame.draw.line(self.win, self.btnsDrawingColor, (420, 1200), (460, 1200), 20)
		pygame.draw.polygon(self.win, self.btnsDrawingColor, ((405, 1200), (435, 1170), (435, 1230)))
		###RIGHT arrow
		pygame.draw.line(self.win, self.btnsDrawingColor, (615, 1200), (660, 1200), 20)
		pygame.draw.polygon(self.win, self.btnsDrawingColor, ((645, 1170), (675, 1200), (645, 1230)))
	
	def drawCursor(self, coorPoints):
		for i in coorPoints:
			x, y=i
			pygame.draw.line(self.win, self.xMarkColor, (x-10, y), (x+10, y), 2)
			pygame.draw.line(self.win, self.xMarkColor, (x, y-10), (x, y+10), 2)
	def makeText(self, fnt_size, txt_n, txt_loc):
		font='freesansbold.ttf'
		basicfnt=pygame.font.Font(font, fnt_size)
		txtSurf=basicfnt.render(txt_n, 1, self.txt_color)
		txtRect=txtSurf.get_rect()
		txtRect.topleft=txt_loc
		self.win.blit(txtSurf, txtRect)
	
	def terminate(self):
		pygame.quit()
		sys.exit()
	def checkForQuit(self):
		for event in pygame.event.get(QUIT):
			self.terminate()
			
def main():
	global fpsclock
	pygame.init()
	n=Tiles(borderColor, winColor, xMarkColor, ctrPntColor, txt_color, btnsDrawingColor, patternColor, borderPatternColor, solvedPuzzleColor1, solvedPuzzleColor2, borderSolvedPuzzleColor, timeLimit, win_bg_color, LightGreen, LightRed, win, puzzleWidth)
	fpsclock=pygame.time.Clock()
	n.win
	while True:
		n.checkForQuit()
		n.draw_board()
		pygame.display.update()
		fpsclock.tick(FPS)