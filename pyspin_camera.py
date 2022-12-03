import PySpin
import signal
import sys

class PySpinCamera:
    def __init__(self):
        # Retrieve singleton reference to system object
        self.system = PySpin.System.GetInstance()
        self.cam_list = self.system.GetCameras()
        num_cameras = self.cam_list.GetSize()
        print('Number of cameras detected: %d' % num_cameras)
        if num_cameras == 0:
            self.cam_list.Clear()
            self.system.ReleaseInstance()
            raise RuntimeError("Not enough cameras")

        self.cam = self.cam_list[0]
        self.nodemap_tldevice = self.cam.GetTLDeviceNodeMap()
        self.cam.Init()
        self.nodemap = self.cam.GetNodeMap()


    def enter_acquisition_mode(self):
        node_acquisition_mode = PySpin.CEnumerationPtr(self.nodemap.GetNode('AcquisitionMode'))
        if not PySpin.IsAvailable(node_acquisition_mode) or not PySpin.IsWritable(node_acquisition_mode):
            print('Unable to set acquisition mode to continuous (enum retrieval). Aborting...')
            return False
        node_acquisition_mode_continuous = node_acquisition_mode.GetEntryByName('Continuous')
        if not PySpin.IsAvailable(node_acquisition_mode_continuous) or not PySpin.IsReadable(node_acquisition_mode_continuous):
            print('Unable to set acquisition mode to continuous (entry retrieval). Aborting...')
            return False
        acquisition_mode_continuous = node_acquisition_mode_continuous.GetValue()
        node_acquisition_mode.SetIntValue(acquisition_mode_continuous)
        print('Acquisition mode set to continuous...')
        self.cam.BeginAcquisition()

    def acquire_image(self):
        image_result = self.cam.GetNextImage()
        if image_result.IsIncomplete():
            print('Image incomplete with image status %d ...' % image_result.GetImageStatus())
        else:
            width = image_result.GetWidth()
            height = image_result.GetHeight()
            stride = image_result.GetStride()
            d = image_result.GetData()
            return d, width, height, stride

    def leave_acquisition_mode(self):
        self.cam.EndAcquisition()

    def __del__(self):
        self.reset_exposure()
        self.reset_gain()

        self.cam.DeInit()
        del self.cam
        self.cam_list.Clear()
        self.system.ReleaseInstance()


    def configure_exposure(self, value):
        try:
            result = True
            # Turn off automatic exposure mode
            if self.cam.ExposureAuto.GetAccessMode() != PySpin.RW:
                print('Unable to disable automatic exposure. Aborting...')
                return False

            self.cam.ExposureAuto.SetValue(PySpin.ExposureAuto_Off)
            print('Automatic exposure disabled...')

            # Set exposure time manually; exposure time recorded in microseconds
            if self.cam.ExposureTime.GetAccessMode() != PySpin.RW:
                print('Unable to set exposure time. Aborting...')
                return False

            # Ensure desired exposure time does not exceed the maximum
            exposure_time_to_set = value
            print(self.cam.ExposureTime.GetMax())
            exposure_time_to_set = min(self.cam.ExposureTime.GetMax(), exposure_time_to_set)
            self.cam.ExposureTime.SetValue(exposure_time_to_set)

        except PySpin.SpinnakerException as ex:
            print('Error: %s' % ex)
            result = False

        return result

    def reset_exposure(self):
        """
        This function returns the camera to a normal state by re-enabling automatic exposure.

        :return: True if successful, False otherwise.
        :rtype: bool
        """
        try:
            result = True

            # Turn automatic exposure back on
            #
            # *** NOTES ***
            # Automatic exposure is turned on in order to return the camera to its
            # default state.

            if self.cam.ExposureAuto.GetAccessMode() != PySpin.RW:
                print('Unable to enable automatic exposure (node retrieval). Non-fatal error...')
                return False

            self.cam.ExposureAuto.SetValue(PySpin.ExposureAuto_Continuous)

            print('Automatic exposure enabled...')

        except PySpin.SpinnakerException as ex:
            print('Error: %s' % ex)
            result = False

        return result


## TODO: finish this and make sure it works

    def configure_gain(self, value):
        
        try:
            result = True
            
            node_gain = PySpin.CFloatPtr(self.nodemap.GetNode('Gain'))
            print(node_gain)
            print('Regular function message:\n\tGain about to be changed to %f...\n' % value)
            node_gain.SetValue(value)

        

        except PySpin.SpinnakerException as ex:
            print('Error: %s' % ex)
            result = False

        return result


    def enable_gain(self):
        """
        This function returns the camera to a normal state by re-enabling automatic exposure.

        :return: True if successful, False otherwise.
        :rtype: bool
        """
        try:
            result = True

            # Turn automatic exposure back on
            #
            # *** NOTES ***
            # Automatic exposure is turned on in order to return the camera to its
            # default state.

            node_gain_auto = PySpin.CEnumerationPtr(self.nodemap.GetNode('GainAuto'))
            node_gain_auto_on = PySpin.CEnumEntryPtr(node_gain_auto.GetEntryByName('On'))

            node_gain_auto.SetIntValue(node_gain_auto_on.GetValue())
            print('Automatic gain disabled...')


        except PySpin.SpinnakerException as ex:
            print('Error: %s' % ex)
            result = False

        return result
    def disable_gain(self):
        """
        This function returns the camera to a normal state by re-enabling automatic exposure.

        :return: True if successful, False otherwise.
        :rtype: bool
        """
        try:
            result = True

            # Turn automatic exposure back on
            #
            # *** NOTES ***
            # Automatic exposure is turned on in order to return the camera to its
            # default state.

            node_gain_auto = PySpin.CEnumerationPtr(self.nodemap.GetNode('GainAuto'))
            node_gain_auto_off = PySpin.CEnumEntryPtr(node_gain_auto.GetEntryByName('Off'))
            node_gain_auto.SetIntValue(node_gain_auto_off.GetValue())
            print('Automatic gain disabled...')


        except PySpin.SpinnakerException as ex:
            print('Error: %s' % ex)
            result = False

        return result
