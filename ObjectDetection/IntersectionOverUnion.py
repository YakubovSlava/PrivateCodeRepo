import torch


def intersection_over_union(boxes_preds, boxes_real, type='corners', unsqueeze=False):

    if unsqueeze:
        boxes_preds = boxes_preds.unsqueeze(0)
        boxes_real = boxes_real.unsqueeze(0)
    if type == 'corners':
        box1_x1, box1_y1, box1_x2, box1_y2 = boxes_preds[..., 0], boxes_preds[..., 1], boxes_preds[..., 2], boxes_preds[..., 3]
        box2_x1, box2_y1, box2_x2, box2_y2 = boxes_real[..., 0], boxes_real[..., 1], boxes_real[..., 2], boxes_real[..., 3]

    else:
        box1_xc, box1_yc, box1_w, box1_h = boxes_preds[..., 0], boxes_preds[..., 1], boxes_preds[..., 2], boxes_preds[..., 3]
        box2_xc, box2_yc, box2_w, box2_h = boxes_real[..., 0], boxes_real[..., 1], boxes_real[..., 2], boxes_real[..., 3]

        box1_x1, box1_y1, box1_x2, box1_y2 = (box1_xc - box1_w / 2, box1_yc - box1_h / 2,
                                              box1_xc + box1_w / 2, box1_yc + box1_h / 2)

        box2_x1, box2_y1, box2_x2, box2_y2 = (box2_xc - box2_w / 2, box2_yc - box2_h / 2,
                                              box2_xc + box2_w / 2, box2_yc + box2_h / 2)

    x1 = torch.max(box1_x1, box2_x1)
    x2 = torch.min(box1_x2, box2_x2)
    y1 = torch.max(box1_y1, box2_y1)
    y2 = torch.min(box1_y2, box2_y2)

    area1 = abs(box1_x2 - box1_x1) * abs(box1_y2 - box1_y1)
    area2 = abs(box2_x2 - box2_x1) * abs(box2_y2 - box2_y1)
    intersection = (x2-x1).clamp(0) * (y2-y1).clamp(0)

    return intersection / (area2+area1-intersection)


if __name__ == "__main__":
    print(intersection_over_union(
        torch.tensor([[0, 0, 3, 2]]),
        torch.tensor([[1, 1, 3, 4]])
    ))

    print(intersection_over_union(
        torch.tensor([[5, 4, 4, 4]]),
        torch.tensor([[3, 2, 2, 2]])
        ,
        type='centers'
    ))
    print(intersection_over_union(
        torch.tensor([[[5, 4, 4, 4]]]),
        torch.tensor([[[3, 2, 2, 2]]])
        ,
        type='centers'
    ))
    print(intersection_over_union(
        torch.tensor([5, 4, 4, 4]),
        torch.tensor([3, 2, 2, 2])
        ,
        type='centers',
    ))
