from packages.schema.tool_models import DriveSearchIn, DriveSearchOut, DriveFile


def search(input: DriveSearchIn) -> DriveSearchOut:
    files = [DriveFile(id="1", name="dummy.txt")]
    return DriveSearchOut(files=files)
