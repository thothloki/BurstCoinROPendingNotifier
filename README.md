# BurstCoin.RO Pending Notifier

This is a desktop notifier app that allows you to see what your pending balance is for the BurstCoin.RO burst pools

If you find value in this app, please consider donating (addresses below)

This was written in Python 3 using PyQt5.

You can run this directly by calling the CGPN.py

Requirements:

GRPC
goburstpool-api-example files (attached)
PyQt5
requests
pip3 install grpcio
pip3 install PyQt5
pip3 install requests

I have included the icon and image files required for this. If you have the release EXE file, please put the RO.jpg file in the same folder as the EXE if you want Shadow's icon to load

On the first close of the app, a settings.ini file will appear. This is holding the settings you had running (Burst Address or Numeric ID, pool selection and custom refresh time).

If you do not select a custom refresh time, it will default to every hour.
