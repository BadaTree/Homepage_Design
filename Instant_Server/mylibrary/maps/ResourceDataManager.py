from mylibrary.maps.MagneticFieldMap import MagneticFieldMap

class ResourceDataManager:
    # wifiDataMap: WiFiDataMap

    def __init__(self, magneticStream, magneticStreamForInstant):
        self.isMagneticMapUsable: bool = False
        self.isWiFiMapUsable: bool = False
        self.noMapMode: bool = False
        self.magneticFieldMap: MagneticFieldMap
        self.instantMap: MagneticFieldMap

        if (magneticStream is not None) and (magneticStreamForInstant is not None):
            self.magneticFieldMap = MagneticFieldMap(magneticStream)
            # self.instantMap = MagneticFieldMap(magneticStreamForInstant)
            self.isMagneticMapUsable = True
        # if (wifiStreamTotal is not None) and (wifiStreamRSSI is not None) and (wifiStreamUnq is not None):
        #     self.wifiDataMap = WiFiDataMap(wifiStreamTotal, wifiStreamRSSI, wifiStreamUnq)
        #     self.isWiFiMapUsable = True
        self.noMapMode = (not self.isMagneticMapUsable) and (not self.isWiFiMapUsable)