from yolov5.detect import run


def process_source_with_model(
    model='yolov5x.pt',  # the biggest one is by default
    source='testing_samples/images/',
    project_path='testing_samples',
    img_sz=(1280, 1280),
    name='.'
):
    run(weights=model,
        source=source,
        save_txt=True,
        imgsz=img_sz,
        max_det=30,
        nosave=True,
        project=project_path,
        name=name,
        device=0
        )

# process_source_with_model(source='VideoSlicer/output/frames/frame103.jpg')