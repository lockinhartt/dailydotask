import re

# Read the file
with open('templates/tasks/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the first </style> tag
first_style_end = content.find('</style>')
if first_style_end == -1:
    print("No </style> tag found!")
    exit(1)

# Find </head> tag
head_end = content.find('</head>')
if head_end == -1:
    print("No </head> tag found!")
    exit(1)

# Remove everything between first </style> and </head>
# Keep the </style> and </head> tags
before_style = content[:first_style_end + len('</style>')]
after_duplicate = content[head_end:]

# Combine
fixed_content = before_style + '\n' + after_duplicate

# Write back
with open('templates/tasks/index.html', 'w', encoding='utf-8') as f:
    f.write(fixed_content)

print("✅ Removed duplicate CSS successfully!")
print(f"Removed {head_end - (first_style_end + len('</style>'))} characters of duplicate CSS")
