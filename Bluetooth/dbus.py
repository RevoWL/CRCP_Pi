import dbus


BUS_NAME = 'org.bluez'
ADAPTER_IFACE = 'org.bluez.Adapter1'
ADAPTER_ROOT = '/org/bluez/hci'
AGENT_IFACE = 'org.bluez.Agent1'
AGNT_MNGR_IFACE = 'org.bluez.AgentManager1'
AGENT_PATH = '/my/app/agent'
AGNT_MNGR_PATH = '/org/bluez'
CAPABILITY = 'KeyboardDisplay'
DEVICE_IFACE = 'org.bluez.Device1'
dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
bus = dbus.SystemBus()

def set_trusted(path):
    props = dbus.Interface(bus.get_object(BUS_NAME, path), dbus.PROPERTIES_IFACE)
    props.Set(DEVICE_IFACE, "Trusted", True)

class Agent(dbus.service.Object):

    @dbus.service.method(AGENT_IFACE,
                         in_signature="", out_signature="")
    def Release(self):
        print("Release")

    @dbus.service.method(AGENT_IFACE,
                         in_signature='o', out_signature='s')
    def RequestPinCode(self, device):
        print(f'RequestPinCode {device}')
        return '0000'

    @dbus.service.method(AGENT_IFACE,
                         in_signature="ou", out_signature="")
    def RequestConfirmation(self, device, passkey):
        print("RequestConfirmation (%s, %06d)" % (device, passkey))
        set_trusted(device)
        return

    @dbus.service.method(AGENT_IFACE,
                         in_signature="o", out_signature="")
    def RequestAuthorization(self, device):
        print("RequestAuthorization (%s)" % (device))
        auth = input("Authorize? (yes/no): ")
        if (auth == "yes"):
            return
        raise Rejected("Pairing rejected")

    @dbus.service.method(AGENT_IFACE,
                         in_signature="o", out_signature="u")
    def RequestPasskey(self, device):
        print("RequestPasskey (%s)" % (device))
        set_tru