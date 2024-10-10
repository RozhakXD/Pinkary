try:
    import mechanize, re, sys, time, threading
    from rich.console import Console
    from rich.text import Text
    from rich import print as printf
    from fake_useragent import UserAgent
except (ModuleNotFoundError):
    print("[!] Some Modules are Missing. Please Install Them Using: `pip install -r requirements.txt`")
    __import__('sys').exit()

def send_views(profile_url, stats):
    try:
        br = mechanize.Browser()
        br.addheaders = [
            ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'),
            ('Accept-Encoding', 'gzip, deflate, br, zstd'),
            ('Accept-Language', 'en-US,en;q=0.9'),
            ('Connection', 'keep-alive'),
            ('Host', 'pinkary.com'),
            ('Sec-Fetch-Dest', 'document'),
            ('Sec-Fetch-Mode', 'navigate'),
            ('Sec-Fetch-Site', 'none'),
            ('Sec-Fetch-User', '?1'),
            ('Upgrade-Insecure-Requests', '1'),
            ('User-Agent', '{}'.format(UserAgent().random))
        ]
        br.set_handle_robots(False)
        response = br.open("{}".format(profile_url)).read()
        time.sleep(1)
        if 'Views' in str(response.decode('utf-8')):
            views = re.search(r'title="(.*?) Views"', str(response.decode('utf-8'))).group(1)
            stats['success'] += 1
            printf(f"[bold white][[bold green]*[bold white]][bold white] Sending[bold green] {stats['success']}[bold white]/[bold green]{views}[bold white] Views...                     ", end='\r')
        else:
            printf("[bold white][[bold red]![bold white]][bold red] Views Failed to Send!               ", end='\r')
            stats['failed'] += 1
    except Exception as e:
        stats['error'] += 1
        printf(f"[bold white][[bold red]![bold white]][bold red] Error: {str(e).title()[:40]}!", end='\r')
        time.sleep(5.0)

def run_views(url, num_requests, num_threads):
    stats = {'success': 0, 'failed': 0, 'error': 0}

    def worker():
        for _ in range(num_requests):
            send_views(url, stats)

    threads = []
    for _ in range(num_threads):
        thread = threading.Thread(target=worker)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print("[bold white]                                    ", end='\r')

    printf(f"[bold white][[bold green]*[bold white]][bold white] Total Success:[bold green] {stats['success']}")
    printf(f"[bold white][[bold yellow]*[bold white]][bold white] Total Failed:[bold yellow] {stats['failed']}")
    printf(f"[bold white][[bold red]*[bold white]][bold white] Total Errors:[bold red] {stats['error']}\n")

if __name__ == "__main__":
    try:
        printf(Text(r""",------. ,--.        ,--.                            
|  .--. '`--',--,--, |  |,-. ,--,--.,--.--.,--. ,--. 
|  '--' |,--.|      \|     /' ,-.  ||  .--' \  '  /  
|  | --' |  ||  ||  ||  \  \\ '-'  ||  |     \   '   
`--'     `--'`--''--'`--'`--'`--`--'`--'   .-'  /    
                                           `---'     """, style="bold magenta"))
        printf("[bold cyan]Pinkary Views Sender - Coded by Rozhak[/bold cyan]\n")

        profile_url = Console().input("[bold white][[bold green]?[bold white]][bold white] Tautan : ")
        count = int(Console().input("[bold white][[bold green]?[bold white]][bold white] Count : "))
        printf("[bold white]                  ")

        num_requests = count
        num_threads = 5

        start_time = time.time()

        run_views(profile_url, num_requests, num_threads)
        printf(f"[bold cyan]Finished in {time.time() - start_time:.2f} Seconds!     ")
        sys.exit()
    except (KeyboardInterrupt):
        sys.exit()