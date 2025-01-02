import asyncio
import threading
from concurrent import futures

import grpc

from internal.app.review_management.usecase import *

import internal.protos.review_management.review_management_pb2 as review_management_pb2
import internal.protos.review_management.review_management_pb2_grpc as review_management_pb2_grpc


class ReviewManagementHandler(review_management_pb2_grpc.ReviewManagementServicer):
    def __init__(self, use_case: ReviewManagementUseCase):
        self.__use_case = use_case

    def create_review(self, request, context):
        def entrypoint():
            asyncio.run(self.__use_case.create_review(
                request.user_id, request.product_id, request.rate, request.text))

        t = threading.Thread(target=entrypoint, daemon=True)
        t.start()
        return review_management_pb2.ReviewOperationResponse(status_code=200)

    def delete_review(self, request, context):
        def entrypoint():
            asyncio.run(self.__use_case.delete_review(
                request.user_id, request.product_id))

        t = threading.Thread(target=entrypoint, daemon=True)
        t.start()
        return review_management_pb2.ReviewOperationResponse(status_code=200)


def serve(use_case: ReviewManagementUseCase, port: str):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    servicer = ReviewManagementHandler(use_case)
    review_management_pb2_grpc.add_ReviewManagementServicer_to_server(
        servicer, server)
    server.add_insecure_port(f"0.0.0.0:{port}")
    server.start()
    server.wait_for_termination()
