import sys; sys.path.append("..")
import inspect
import uuid

import yaml

import config.paths as PATHS


def save_clf_config(
        clf: object,
        description: str,
        name: str | None = None,
        id: str | None = None,
        creation_str: str | None = None,
        imports: str | None = None
    ) -> None:
    cfg = create_clf_config(
        clf, description, name, id, creation_str, imports
    )
    with open(
        (PATHS.MODELS_CONFIG / cfg["id"]).with_suffix('.yaml'),
        'w') as f:
        yaml.dump(cfg, f, default_flow_style=False)


def create_clf_config(
        clf: object,
        description: str,
        name: str | None = None,
        id: str | None = None,
        creation_str: str | None = None,
        imports: str | None = None
    ) -> dict:
    cfg = dict()
    cfg["description"] = description
    cfg["name"] = name if name else clf.__class__.__name__
    cfg["id"] = id if id else f"{cfg['name']}_{uuid.uuid4()}"
    cfg["imports"] = imports if imports else inspect.getmodule(clf).__name__

    if creation_str:
        cfg["creation_str"] = creation_str
    else:
        imports = cfg["imports"]
        clf_repr = __filter_whitespace(repr(clf))
        cfg["creation_str"] = f"{imports}.{clf_repr}"

    return cfg


def __filter_whitespace(text: str):
    return "".join(filter(
        lambda w : not w.isspace(),
        text
    ))
