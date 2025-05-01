#! /usr/bin/python3

from enum import Enum
import subprocess as sp
import datetime
import yaml


file_name = "version"


class Filetype(Enum):
    C_FILE = 1
    TXT_FILE = 2
    JSON_FILE = 3
    YMAL_FILE = 4


def run_git_cmds(cmd):
    full_cmd = ["git"]

    for i in range(len(cmd)):
        full_cmd.append(cmd[i])

    ret = sp.run(full_cmd, capture_output=True)
    if ret.returncode != 0:
        print(f"Faild to execute the cmd {ret.args}, got error code {ret.returncode}")
        if ret.stderr:
            print(f"Error {ret.stderr.decode('utf-8')}")
        if ret.stdout:
            print(f" {ret.stdout.decode('utf-8')}")
        return None

    return ret.stdout.decode().strip("\n")


def gen_version_file(info: dict, type: Filetype):

    match type:
        case Filetype.C_FILE:
            print("Generating version.h file")

            with open(f"{file_name}.h", "w") as f:
                f.write("/* This file was auto generated from VTrace. */\n\n")
                f.write("#pragma once\n\n")
                f.write(f'#define TIMESTAMP         "{info["Commit Timestamp"]}"\n')
                f.write(f'#define GIT_BRANCH        "{info["Git Branch"]}"\n')
                f.write(f'#define GIT_DESCRIBE      "{info["Git Describe"]}"\n')
                f.write(f'#define GIT_SHA           "{info["Git Sha"]}"\n')
                f.write(f'#define GIT_SHA_SHORT     "{info["Git Sha-short"]}"\n')
                f.write(f'#define GIT_TAG           "{info["Git Tag"]}"\n')

        case Filetype.TXT_FILE:
            print("Generating version.txt file")
            return

        case Filetype.JSON_FILE:
            print("Generating version.json file")
            return

        case Filetype.YMAL_FILE:
            print("Generating version.yml file")

            with open(f"{file_name}.yml", "w") as file:
                file.write("# This file was auto generated from VTrace.\n\n")
                yaml.dump(info, file, indent=4)
            return

    pass


if __name__ == "__main__":

    tag = run_git_cmds(
        ["describe", "--tags"],
    )
    git_desc = run_git_cmds(
        ["describe", "--always", "--long", "--tags", "--broken", "--dirty"],
    )

    branch_name = run_git_cmds(
        ["rev-parse", "--abbrev-ref", "HEAD"],
    )

    sha_short = run_git_cmds(
        ["rev-parse", "--short", "HEAD"],
    )

    sha = run_git_cmds(
        ["rev-parse", "HEAD"],
    )

    time_stamp = str(datetime.datetime.now())

    # print(f"git describe:  {git_desc}")
    # print(f"git branch:    {branch_name}")
    # print(f"git sha:       {sha}")
    # print(f"git sha short: {sha_short}")
    # print(f"Time:          {time_stamp}")
    # print(f"git tags:      {tag}")

    info = {
        "Git Describe": git_desc,
        "Git Branch": branch_name,
        "Git Sha": sha,
        "Git Sha-short": sha_short,
        "Git Tag": tag,
        "Commit Timestamp": time_stamp,
    }

    gen_version_file(info, Filetype.YMAL_FILE)
    gen_version_file(info, Filetype.C_FILE)
