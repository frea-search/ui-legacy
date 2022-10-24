#!/bin/sh
rm -f /var/frea/tmp/org.freasearch.intelligence-engine/weather.sock
su frea -c "python3 /var/frea/subsystems/org.freasearch.intelligence-engine/weather.py"
