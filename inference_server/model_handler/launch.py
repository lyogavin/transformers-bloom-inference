import argparse

import torch.distributed as dist

from ..models import get_model_class
from ..utils import get_argument_parser, parse_args
from .grpc_utils.generation_server import serve


def get_args() -> argparse.Namespace:
    parser = get_argument_parser()

    group = parser.add_argument_group(title="launch config")
    group.add_argument("--local_rank", required=False, type=int, help="used by dist launchers")
    group.add_argument("--cpu_offload", action="store_true", help="whether to activate CPU offload for DS ZeRO")
    group.add_argument("--port", type=int, help="GRPC port")

    args = parse_args(parser)

    return args


def main():
    args = get_args()
    model = get_model_class(args.deployment_framework)(args)
    serve(model, args.port + dist.get_rank())


if __name__ == "__main__":
    main()