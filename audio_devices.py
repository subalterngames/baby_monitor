import sounddevice as sd

input_devices = []
output_devices = []
for device_description in sd.query_devices():
    if device_description["max_input_channels"] > 0:
        input_devices.append(device_description["name"])
    else:
        output_devices.append(device_description["name"])

print("INPUT:")
print("\n".join(input_devices))
print("")
print("OUTPUT:")
print("\n".join(output_devices))
