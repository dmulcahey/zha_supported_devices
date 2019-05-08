import os
import logging
import yaml

_LOGGER = logging.getLogger(__name__)

def generate_device_page(template_path):
    device = {}
    with open(template_path + '/device.yaml', "r") as device_file:
        device = yaml.load(device_file)
    with open('../md_template.txt', "r") as header_template:
        template_string = header_template.read()
        output = template_string.format(
            device['manufacturer'],
            device['model'],
            device['link'],
            template_path + '/' + device['picture'],
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
    


pages = next(os.walk('../devices'))[1] # get just sub directories
for page in pages:
    devices = next(os.walk('../devices/' + page))[1]
    for device in devices:
        generate_device_page('../devices/' + page + '/' + device)

