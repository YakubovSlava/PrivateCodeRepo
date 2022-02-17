import torch
from collections import Counter
from IntersectionOverUnion import intersection_over_union


def mean_average_precision(
        pred_boxes,
        true_boxes,
        iou_threshold=0.5,
        box_format='corners',
        num_classes=20
):
    average_precisions = []
    epsilon = 1e-6

    for c in range(num_classes):
        detections = []
        ground_truths = []

        for detection in pred_boxes:
            if detection[1] == c:
                detections.append(detection)

        for true_box in true_boxes:
            if true_box[1] == c:
                ground_truths.append(true_box)

        amount_bboxes = Counter([gt[0] for gt in ground_truths])

        for key, val in amount_bboxes.items():
            amount_bboxes[key] = torch.zeros(val)

        detections.sort(key=lambda x: x[2], reverse=True)

        tp = torch.zeros(len(detections))
        fp = torch.zeros(len(detections))
        total_true_boxes = len(ground_truths)

        for detection_id, detection in enumerate(detections):
            ground_truths_img = [bbox for bbox in ground_truths if bbox[0] == detection[0]]
            num_gts = len(ground_truths_img)
            best_iou = 0

            for idx, gt in enumerate(ground_truths_img):
                iou = intersection_over_union(
                    torch.tensor(detection[3:]),
                    torch.tensor(gt[3:]),
                    type=box_format,
                    unsqueeze=True
                )

                if iou > best_iou:
                    best_iou = iou
                    best_gt_index = idx

            if best_iou > iou_threshold:
                if amount_bboxes[detection[0]][best_gt_index] == 0:
                    tp[detection_id] = 1
                    amount_bboxes[detection[0]][best_gt_index] = 1
                else:
                    fp[detection_id] = 1
            else:
                fp[detection_id] = 1

        tp_cumsum = torch.cumsum(tp, dim=0)
        fp_cumsum = torch.cumsum(fp, dim=0)

        recalls = tp_cumsum/(total_true_boxes+epsilon)
        precisions = tp_cumsum/(tp_cumsum+fp_cumsum+epsilon)

        precisions = torch.cat((torch.tensor([1]), precisions))
        recalls = torch.cat((torch.tensor([0]), recalls))

        average_precisions.append(torch.trapz(precisions, recalls))

    return sum(average_precisions)/len(average_precisions)
    # return (average_precisions, precisions, recalls)



if __name__ == '__main__':
    print(
        mean_average_precision(
            [
                [0, 1, 0.6, 0, 0, 3, 4],
                [0, 1, 0.6, 3.5, 4.5, 4.5, 5.5]
            ],
            [
                [0, 0, 0.6, 0, 0, 3, 4],
                [0, 1, 0.6, 3.5, 4.5, 4.5, 5.5]
            ],
            0.5,
            'corners',
            2
        )
    )