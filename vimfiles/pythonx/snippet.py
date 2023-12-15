import vim

def func_header_snippet(row):
    cmt = "//!"
    cb = vim.current.buffer
    start = row
    while start >= 0:
        line = cb[start-1].strip()
        if not line.startswith(cmt):
            break
        start -= 1



    print("HDR")

def select_snippet(line):
    line = line.strip()
    if line.startswith("//!"):
        return func_header_snippet

def main():
    row, col = vim.current.window.cursor
    row -= 1
    cline = vim.current.buffer[row]

    func = select_snippet(cline)
    if func:
        func(row)
#! @brief
#! @details


main()
