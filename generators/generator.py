import os
import logging
import yaml
from shutil import copyfile

_LOGGER = logging.getLogger(__name__)

def generate_device_page(template_path, manufacturer, device_model):
    device = {}
    with open(template_path + '/device.yaml', "r") as device_file:
        device = yaml.load(device_file)
    with open('../md_template.txt', "r") as header_template:
        template_string = header_template.read()
        output = template_string.format(
            device['manufacturer'],
            device['model'],
            device['link'],
            './' + device['picture'],
            device['description'],
        )
        sensor_string = ""
        for domain in device['domains']:
            for sensor in domain['entities']:
                sensor_string += '{} - {}\n\n'.format(
                    sensor,
                    domain['name']
                )
        output += sensor_string
        if os.path.exists(template_path + "/events"):
            events_text = generate_events(template_path + "/events")
            output += events_text
            print(output)
    filename = "../output/devices/" + manufacturer + '/' + device_model + '.md'
    try:
        os.makedirs(os.path.dirname(filename))
    except:
        pass
    device_file = open(filename, "w")
    device_file.write(output)
    device_file.close()

    copyfile(template_path + '/' + device['picture'], '../output/devices/' + manufacturer + '/' + device['picture'])
    return device['model']

def generate_events(events_path):
    events_text = '# Events\n\n'
    event_files = os.listdir(events_path)
    for event_file in event_files:
        full_path = events_path + '/' + event_file
        file_content = open(full_path, 'r').read()
        events_text += '## ' + os.path.splitext(os.path.basename(full_path))[0] + '\n\n'
        events_text += '```json\n'
        events_text += file_content
        events_text += '\n'
        events_text += '```\n\n'
    return events_text
    


manufacturers = next(os.walk('../devices'))[1] # get just sub directories
index_content = '# ZHA - Supported Devices\n\n'

for manufacturer in manufacturers:
    index_content += '## ' + manufacturer + '\n\n'
    devices = next(os.walk('../devices/' + manufacturer))[1]
    for device in devices:
        index_content += '[' + generate_device_page('../devices/' + manufacturer + '/' + device, manufacturer, device) + '](./devices/' + manufacturer + '/' + device + '.md)\n\n'
print(index_content)
index_file = open("../output/index.md", "w")
index_file.write(index_content)
index_file.close()
