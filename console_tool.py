import curses
import subprocess


def main(stdscr):
    curses.curs_set(1)
    stdscr.clear()
    max_y, max_x = stdscr.getmaxyx()
    input_win = curses.newwin(1, max_x, max_y - 1, 0)
    output_win = curses.newwin(max_y - 1, max_x, 0, 0)
    output_lines = []

    while True:
        output_win.clear()
        start_line = max(0, len(output_lines) - (max_y - 1))
        for i, line in enumerate(output_lines[start_line:], 0):
            output_win.addstr(i, 0, line[:max_x-1])
        output_win.refresh()
        input_win.clear()
        input_win.refresh()
        curses.echo()
        command = input_win.getstr(0, 0).decode('utf-8')
        curses.noecho()
        if command in ['exit', 'quit']:
            break
        if command:
            try:
                result = subprocess.run(command, shell=True, text=True, capture_output=True)
                output_lines.extend((result.stdout + result.stderr).splitlines())
            except Exception as e:
                output_lines.append(f"Error: {e}")


def run():
    curses.wrapper(main)


if __name__ == '__main__':
    run()
