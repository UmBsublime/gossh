import asyncio, asyncssh, subprocess, sys

# http://asyncssh.readthedocs.io/en/latest/api.html#asyncssh.SSHServer.begin_auth
# http://asyncssh.readthedocs.io/en/latest/api.html#create-server
# xinetd, shellinabox
# binary websocket
# https://nyancat.dakko.us/
async def handle_client(process):
    print("A player has joined")

    bc_proc = subprocess.Popen('/mnt/c/Users/Sublime/PycharmProjects/gossh/venv/bin/python3' 
                               ' /mnt/c/Users/Sublime/PycharmProjects/gossh/go.py', shell=True, stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    await process.redirect(stdin=bc_proc.stdin, stdout=bc_proc.stdout,
                           stderr=bc_proc.stderr)
    await process.stdout.drain()
    print("A player has quit")
    process.exit(0)


async def start_server():
    await asyncssh.listen('', 8022, server_host_keys=['test_rsa.key'],
                          process_factory=handle_client)

if __name__ == "__main__":

    loop = asyncio.get_event_loop()

    try:
        loop.run_until_complete(start_server())
    except (OSError, asyncssh.Error) as exc:
        sys.exit('Error starting server: ' + str(exc))

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        sys.exit('Server stopped')
