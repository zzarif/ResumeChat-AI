import html
import re


def validate_files(uploaded_files):
    invalid_files = []
    for file in uploaded_files:
        if file.type != "application/pdf":
            invalid_files.append((file.name, "Not a PDF file"))
        elif file.size > 20 * 1024 * 1024:  # 20MB in bytes
            invalid_files.append((file.name, "Exceeds 20MB limit"))
    return invalid_files


def format_response(text, include_cursor=False):
    # Escape HTML characters
    text = html.escape(text)

    # Split the text into lines
    lines = text.split('\n')
    formatted_lines = []
    list_type = None
    list_count = 0
    in_list = False

    for i, line in enumerate(lines):
        # Check for numbered list
        numbered_match = re.match(r'^(\d+)\.\s(.+)$', line)
        # Check for bullet point list
        bullet_match = re.match(r'^[-*]\s(.+)$', line)

        if numbered_match or bullet_match:
            if not in_list:
                if list_type:
                    formatted_lines.append(f'</{list_type}>')
                list_type = 'ol' if numbered_match else 'ul'
                formatted_lines.append(f'<{list_type}>')
                in_list = True
                list_count = int(numbered_match.group(1)
                                 ) if numbered_match else 0

            if numbered_match:
                if int(numbered_match.group(1)) != list_count:
                    formatted_lines.append(f'<li value="{numbered_match.group(1)}">{
                                           numbered_match.group(2)}</li>')
                else:
                    formatted_lines.append(
                        f'<li>{numbered_match.group(2)}</li>')
                list_count += 1
            else:
                formatted_lines.append(f'<li>{bullet_match.group(1)}</li>')
        else:
            if in_list:
                formatted_lines.append(f'</{list_type}>')
                in_list = False
                list_type = None
            formatted_lines.append(line)

            # Add line break if it's not the last line and we're not in a list
            if i < len(lines) - 1 and not in_list:
                formatted_lines.append('<br>')

    if in_list:
        formatted_lines.append(f'</{list_type}>')

    formatted_text = ''.join(formatted_lines)

    if include_cursor:
        formatted_text += '<span class="blinking-cursor">▌</span>'

    return formatted_text
