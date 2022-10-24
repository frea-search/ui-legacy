#!/bin/sh
rm -rf /tmp/org.freasearch.intelligence-engine
su frea -c "python3 /var/frea/subsystems/org.freasearch.intelligence-engine/weather.py"
