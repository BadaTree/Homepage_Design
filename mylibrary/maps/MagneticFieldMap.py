from typing import List, Dict

class MagneticFieldMap():


    def __init__(self, inputStream):
        self.floorIndex: List[List[str]] = []
        self.pos: List[int] = []
        self.mag: Dict[int, List[float]] = {}
        self.mapWidth: int = 0
        self.mapHeight: int = 0
        # init #
        splitData = []
        x = 0
        y = 0
        index = 0

        with open(inputStream, "r") as f:
            while True:
                it = f.readline()
                if not it:
                    break
                splitData = it.split("\t")
                x = int(splitData[0])
                y = int(splitData[1])
                index = x * 10000 + y
                self.mag[index] = [float(splitData[2]), float(splitData[3]), float(splitData[4])]
                self.pos.append(index)
                if (x > self.mapWidth):
                    self.mapWidth = x
                if (y > self.mapHeight):
                    self.mapHeight = y

    def getWidth(self):
        return self.mapWidth

    def getHeight(self):
        return self.mapHeight


    def getData(self, dx, dy):
        try:
            return self.mag[10000 * int(round(dx)) + int(round(dy))]
        except:
            # return (0.0, 0.0, 0.0)
            return (-10000.0, -10000.0, -10000.0)

    def isPossiblePosition(self, dx, dy):
        x = int(round(dx))
        y = int(round(dy))
        if (10000*x + y) not in self.mag:
            return False
        elif (x < 0) or (y < 0):
            return False
        elif (x >= self.mapWidth) or (y >= self.mapHeight):
            return False
        else:
            return True

    def isPossiblePosition2(self, dx, dy):
        x = int(round(dx))
        y = int(round(dy))
        if (x < 0) or (y < 0):
            return False
        elif (x > self.mapWidth) or (y > self.mapHeight):
            return False
        else:
            return True