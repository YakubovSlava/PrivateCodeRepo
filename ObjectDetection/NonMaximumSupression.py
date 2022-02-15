import torch
from IntersectionOverUnion import intersection_over_union


def non_maximum_suppression(
        prediction,
        iou_threshold,
        probability_threshold,
        box_format='corners'):

    bboxes = [box.unsqueeze(0) for box in prediction if box[1] > probability_threshold]
    bboxes = sorted(bboxes, key=lambda x: x[:, 1], reverse=True)
    bboxes = torch.cat(bboxes, dim=0)
    bboxes_after_nms = []

    while bboxes.shape[0] != 0:
        curr_box = bboxes[0]
        bboxes = torch.tensor([box.tolist() for box in bboxes[1:] if
                               (box[0].item() != curr_box[0].item() or
                                intersection_over_union(curr_box[2:].unsqueeze(0), box[2:].unsqueeze(0), type=box_format)[0] <
                                iou_threshold)])
        bboxes_after_nms.append(curr_box.tolist())

    return torch.tensor(bboxes_after_nms)


if __name__ == '__main__':

    print(non_maximum_suppression(
        torch.tensor([[0, 0.9, 0, 0, 1, 1],
                      [1, 0.8, 0, 0, 1, 1],
                      [0, 0.1, 0, 0, 10, 10],
                      [0, 0.8, 0, 0, 1, 1]]),
        0.5,
        0.5
    ))
