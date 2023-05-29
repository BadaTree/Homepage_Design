from mylibrary.instant.InstantLocalization import InstantLocalization
from mylibrary.maps.ResourceDataManager import ResourceDataManager

class ExIndoorLocalization():
    def __init__(self, magnetic_stream, magnetic_stream_instant):
        self.resource_data_manager = ResourceDataManager(magnetic_stream, magnetic_stream_instant)

        # my_angle = 0
        # self.instantLocalization = InstantLocalization(self.resource_data_manager.magneticFieldMap, magnetic_stream_instant, list(range(my_angle, my_angle + 1, 10)))
        self.instantLocalization = InstantLocalization(self.resource_data_manager.magneticFieldMap, magnetic_stream_instant, list(range(0, 360, 10)))

        self.gyro_from_map_collection = 0
        self.sampled_yaw_angle = 0
        self.yaw_cali_value = 0

        # Instant Localization related
        self.current_position = []
        self.localizationResult = {
            "status_code": 0.0,
            "is_gyro_reset": 0.0,
            "gyro_from_map": -1.0,
            "pos_x": -1.0,
            "pos_y": -1.0,
            "matching_level": 0.0,
            "step_count": 0.0
        }

        self.stepCount = 0
        self.magneticQueue = []

    def sensorChanged(self, test_data_df):
        self.sampled_yaw_angle = float(test_data_df[5])
        self.gyro_from_map_collection = self.sampled_yaw_angle - self.yaw_cali_value
        if len(test_data_df) <= 7:
            self.magneticQueue.append(list(test_data_df[2:5]) + [test_data_df[6], self.gyro_from_map_collection])
        else:
            try:
                self.magneticQueue.append(list(test_data_df[2:5]) + [test_data_df[6], self.gyro_from_map_collection] + test_data_df[7:].tolist())
            except:
                self.magneticQueue.append(list(test_data_df[2:5]) + [test_data_df[6], self.gyro_from_map_collection] + test_data_df[7:])

        self.LocalizationThread()

    ### 쓰레드 ###
    def LocalizationThread(self):
        if len(self.magneticQueue) > 0:
            inputData = self.magneticQueue.pop()
            search_range = [0,800,0,800]

            self.localizationResult = self.instantLocalization.getLocation(
                magx=inputData[0],
                magy=inputData[1],
                magz=inputData[2],
                stepLength=inputData[3],
                gyro_from_map=inputData[4],
                search_range = search_range
            )


    def gyroReset(self, reset_gyro: float, engine_num: int = 1):
        self.yaw_cali_value = ((self.sampled_yaw_angle - reset_gyro) + 360) % 360

