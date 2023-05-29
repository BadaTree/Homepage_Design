from math import *
import random
from typing import List

from mylibrary.filters.Particle import Particle
from mylibrary.maps.MagneticFieldMap import MagneticFieldMap


class ParticleFilter():
    def __init__(self, map: MagneticFieldMap, particleCount: int, posX: int, posY: int, maxR: int):
        self.map: MagneticFieldMap = map
        self.particles: List[Particle] = []
        self.particleCount = particleCount
        self.try_pf_in_no_map_area: bool = False

        # init #
        x: int = 0
        y: int = 0
        count: int = 0
        rR = maxR
        for i in range(self.particleCount):
            while True:
                x = random.randint(0, 2 * rR - 1) + posX - rR
                y = random.randint(0, 2 * rR - 1) + posY - rR
                # count += 1
                # if count > 30:
                #     rR += 10
                #     count = 0
                if map.isPossiblePosition(x, y):
                    break

            self.particles.append(Particle(x, y, random.randint(0, 359), 1.0 / particleCount))

    def step(self, sensorValues: List[float], heading: float, stepLength: float, state: int = 0,
             pdrModeOn: bool = False, curPosition: List[float] = [0.0, 0.0]) -> List[float]:
        pdrModeOn = pdrModeOn
        x = 0.0
        y = 0.0
        w = 0.0
        if not pdrModeOn:
            if not self.map.isPossiblePosition(curPosition[0], curPosition[1]):
                pdrModeOn = True
                self.try_pf_in_no_map_area = True
            else:
                self.try_pf_in_no_map_area = False
        else:
            self.try_pf_in_no_map_area = False

        self.moveParticles(stepLength, heading)
        # self.applyObservation(sensorValues)
        for p in self.particles:
            w += p.w
            x += p.x * p.w
            y += p.y * p.w

        x /= w
        y /= w

        self.particles = self.resample(self.particles, heading)
        if not pdrModeOn:
            self.blocking(x, y, stepLength)
        return [x, y]

    def moveParticles(self, stepLength: float, heading: float, state: int = 0, pdrModeOn: bool = False):
        r: float
        x: float
        y: float
        stepNoise: int
        headingNoise: int

        if not pdrModeOn:
            for p in self.particles:
                while True:
                    if state > 0:
                        stepNoise = random.randint(0, 5) - 2
                        headingNoise = random.randint(0, 11) - 3
                    else:
                        stepNoise = random.randint(0, 5) - 2
                        headingNoise = random.randint(0, 11) - 5
                    r = (heading + headingNoise) % 360
                    x = round(p.x + sin(radians(r)) * ((stepLength * 10) + stepNoise))
                    y = round(p.y + cos(radians(r)) * ((stepLength * 10) + stepNoise))

                    if x >= self.map.getWidth():
                        x = self.map.getWidth()
                    elif x <= 0:
                        x = 0.0

                    if y >= self.map.getHeight():
                        y = self.map.getHeight()
                    elif y <= 0:
                        y = 0.0

                    if self.map.isPossiblePosition2(x, y):
                        break
                p.a = r
                p.x = x
                p.y = y
        else:
            for p in self.particles:
                while True:
                    r = heading % 360
                    x = round(p.x + sin(radians(r)) * stepLength * 10)
                    y = round(p.y + cos(radians(r)) * stepLength * 10)

                    if x >= self.map.getWidth():
                        x = self.map.getWidth()
                    elif x <= 0:
                        x = 0.0

                    if y >= self.map.getHeight():
                        y = self.map.getHeight()
                    elif y <= 0:
                        y = 0.0

                    if self.map.isPossiblePosition2(x, y):
                        break
                p.a = r
                p.x = x
                p.y = y

    def applyObservation(self, sensorValues):
        for p in self.particles:
            mapData = self.map.getData(p.x, p.y)
            errX = sensorValues[0] - mapData[0]
            errY = sensorValues[1] - mapData[1]
            errZ = sensorValues[2] - mapData[2]
            p.w = exp(-1 * (pow(errX, 2) / 200)) + exp(-1 * (pow(errY, 2) / 200)) + exp(-1 * (pow(errZ, 2) / 200))

    def resample(self, p, angle):
        newParticles : List[Particle] = []
        B = 0.0
        best = self.getBestParticle(p)
        index = int(random.random() * self.particleCount)
        for i in range(self.particleCount):
            B += random.random() * 2 * best.w
            while B > p[index].w:
                B -= p[index].w
                index = self.circle(index + 1, self.particleCount)
            newParticles.append(Particle(round(p[index].x), round(p[index].y), angle, 1.0 / self.particleCount))
        return newParticles

    def circle(self, n, length):
        num = n
        while num > length - 1:
            num -= length
        while num < 0:
            num += length
        return num

    def getBestParticle(self, particles):
        particle = particles[0]
        for p in particles:
            if p.w > particle.w:
                particle = p
            else:
                particle = particle
        return particle

    def blocking(self, x, y, stepLength):
        count = 0
        area = round((stepLength * 10) * 6)
        if area == 0:
            area = 30
        for p in self.particles:
            while not self.map.isPossiblePosition(p.x, p.y):
                p.x = random.randint(0, area - 1) + x - area / 2
                p.y = random.randint(0, area - 1) + y - area / 2
                count += 1
                if count > 30:
                    area += 10
                    count = 0
