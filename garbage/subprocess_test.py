import subprocess

test = subprocess.run(['ddcutil', 'get', '10', '--terse', '--sleep-multiplier', str('.03')], capture_output=True)


