import torch

[[1,2,3,4]]

def IoU(boxes_preds, boxes_real):

    box1_x1, box1_y1, box1_x2, box1_y2 = boxes_preds[:, 0], boxes_preds[:, 1], boxes_preds[:, 2], boxes_preds[:, 3]
    box2_x1, box2_y1, box2_x2, box2_y2 = boxes_real[:, 0], boxes_real[:, 1], boxes_real[:, 2], boxes_real[:, 3]

    x1 = torch.max(box1_x1, box2_x1)
    x2 = torch.min(box1_x2, box2_x2)
    y1 = torch.max(box1_y1, box2_y1)
    y2 = torch.min(box1_y2, box2_y2)

    intersection = (x2-x1).clamp(0) * (y2-y1).clamp(0)

    return None