Automation Case Studies
=======================

Collection of basic case studies to allow development of a common architecure of hardware
software for instrument and site automation.

1) Focus on each task to be done like turn the cal lamp on,
   turn the call lamp off, etc,

2) To develop a few bits of code for each function that will include
   a class/code for that task to run in both python and C++.

3) Each task will have messages for actions and to report both
   status, warnings and errors.

I want to ignore the transport layer as much as possible. I like
RS-232 for the OTA and any other standard for the rest of the world.

Sugest dividing the world into telescope/instrumentation, observatory
control, and then to the sensors for temperature, humidity and
other factors as they come along.
