from parser.main_func import main
# url = "https://minio-endpoint.skilldify.ai/armss-dev/%5B274%5D-a823eccafb16c1cc08357e6a0460509236a1f30cd2824eb48324eaf01d7a4bf7%21%40%26all-design-guidelines.pdf?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=gNT1ijYwEy1ZcEmX%2F20240606%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20240606T025013Z&X-Amz-Expires=86400&X-Amz-SignedHeaders=host&X-Amz-Signature=06bfa9893ac15691fb22cd547ce1415e5ac679d1057cebe16fcb32c7d5a84f10"
url ="https://minio-endpoint.exitest.com/armss-dev/%5B502%5D-2efe441463c130d8a0363e729e41564ee6ead2c5a40ad3e22491962663040227%21%40%26CV_New_AKSINGH.pdf?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=3G1coIOGQpk2Yvrxp9Ao%2F20240613%2Fap-south-1%2Fs3%2Faws4_request&X-Amz-Date=20240613T092759Z&X-Amz-Expires=86400&X-Amz-SignedHeaders=host&X-Amz-Signature=fb0cc0851c91a2a66508bf96ca803e1085c625de86e99e41759dbe3f210ffe3b"


# from main import handleUpload

# handleUpload("[321]-1c0a5080dc5c5d34ec782a034e2d1850eafad60fb4ebb3971ae5c530cbcf00da!@&Resume 1.png")



main(url, "check", 2)
# from parser.text_extractor import tika_text_extraction

# fil = "P:/Bhagyashri/Resume/1666925242344_CustCopy2.pdf"
# print(tika_text_extraction(fil))