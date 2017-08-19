import main as m
import os
import hashlib
from shutil import copyfile

rawplans = os.listdir(m.RAWPLANS_UPLOAD_DIR)

print type(rawplans)
for plan in rawplans:
    sha1 = hashlib.sha1()
    filepath = os.path.join(m.RAWPLANS_UPLOAD_DIR,plan)
    with open(filepath, 'rb') as f:
        data = f.read()
        sha1.update(data)
        hash = sha1.hexdigest()
    planfile = "{0}.plan.png".format(hash)
    planfile_fullpath = os.path.join(m.PLANS_UPLOAD_DIR, planfile)

    if not os.path.isfile(planfile_fullpath):
        copyfile(filepath, planfile_fullpath)

print os.listdir(m.PLANS_UPLOAD_DIR)