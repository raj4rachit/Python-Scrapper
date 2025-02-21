from reactpy import component, html, run

@component
def DataList(items, filter_by_priority=None, sort_by_priority=False):
    if filter_by_priority is not None:
        items = [i for i in items if i["priority"] <= filter_by_priority]
    if sort_by_priority:
        items = sorted(items, key=lambda i: i["priority"])
    list_item_elements = [html.li({"key": i["id"]}, i["text"]) for i in items]
    return html.ul(list_item_elements)


@component
def TodoList():
    tasks = [
        {"id": 0, "text": "Make breakfast", "priority": 0},
        {"id": 1, "text": "Feed the dog", "priority": 0},
        {"id": 2, "text": "Do laundry", "priority": 2},
        {"id": 3, "text": "Go on a run", "priority": 1},
        {"id": 4, "text": "Clean the house", "priority": 2},
        {"id": 5, "text": "Go to the grocery store", "priority": 2},
        {"id": 6, "text": "Do some coding", "priority": 1},
        {"id": 7, "text": "Read a book", "priority": 1},
    ]
    return html.section(
        html.div(
            {"class_name": "container"},
            html.h1({"class_name": "title"}, "My Todo List"),
            html.ul(
                {"class_name": "list"},
                html.li({"class_name": "item"}, "Build a cool new app"),
                html.li({"class_name": "item"}, "Share it with the world!"),
            ),
        ),
        DataList(tasks, filter_by_priority=1, sort_by_priority=True),
    )


run(TodoList)