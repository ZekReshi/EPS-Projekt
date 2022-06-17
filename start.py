import sys

if len(sys.argv) > 1:
    arg = sys.argv[1]
    if arg == 'camera':
        import Sensors.Camera as camera
        camera.main()
    if arg == 'sound':
        import Actuators.Actuator_Sound as sound
        sound.main()
    if arg == 'blink':
        import Actuators.Actuator_Blink as blink
        blink.main()
