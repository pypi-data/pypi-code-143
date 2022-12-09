# Copyright 2021 Open Logistics Foundation
#
# Licensed under the Open Logistics License 1.0.
# For details on the licensing terms, see the LICENSE file.

"""Module for parsing MOT formatted annotations"""

import logging
import os
from typing import Dict, List

import cv2

from mlcvzoo_base.api.data.annotation import BaseAnnotation
from mlcvzoo_base.api.data.annotation_class_mapper import AnnotationClassMapper
from mlcvzoo_base.api.data.annotation_parser import AnnotationParser
from mlcvzoo_base.configuration.annotation_handler_config import (
    AnnotationHandlerMOTInputDataConfig,
)
from mlcvzoo_base.configuration.class_mapping_config import (
    ClassMappingConfig,
    ClassMappingModelClassesConfig,
)
from mlcvzoo_base.data_preparation.annotation_builder.mot_annotation_builder import (
    MOTAnnotationBuilder,
)
from mlcvzoo_base.data_preparation.structs import MOTChallengeFormats
from mlcvzoo_base.utils.file_utils import get_file_list

logger = logging.getLogger(__name__)


class MOTAnnotationParser(AnnotationParser):
    """
    Class for parsing annotations in MOT challenge format.
    Please see MOTChallengeFormats for supported formats.
    """

    def __init__(
        self,
        mapper: AnnotationClassMapper,
        mot_input_data: List[AnnotationHandlerMOTInputDataConfig],
    ) -> None:
        AnnotationParser.__init__(self, mapper=mapper)

        self.mot_input_data = mot_input_data

    @staticmethod
    def create_mot_mapper(mot_format: str) -> AnnotationClassMapper:

        if mot_format == MOTChallengeFormats.MOT20.value:
            mot_class_mapper = AnnotationClassMapper(
                class_mapping=MOTAnnotationParser.create_mot__2020_class_mapping()
            )
        elif mot_format == MOTChallengeFormats.MOT1617.value:
            mot_class_mapper = AnnotationClassMapper(
                class_mapping=MOTAnnotationParser.create_mot__201617_class_mapping()
            )
        elif mot_format == MOTChallengeFormats.MOT15.value:
            mot_class_mapper = AnnotationClassMapper(
                class_mapping=MOTAnnotationParser.create_mot__2015_class_mapping()
            )
        else:
            raise ValueError(
                f"mot_format='{mot_format}' not valid. "
                f"Please use one of "
                f"{[f.value for f in MOTChallengeFormats]}"
            )

        return mot_class_mapper

    def parse(self) -> List[BaseAnnotation]:
        """
        Parse a list of annotations from a MOT annotation file.
        Details of parsing the different formats can be found in
        mlcvzoo_base.data_preparation.annotation_builder.mot_annotation_builder

        Returns:
            A list of BaseAnnotation objects
        """

        annotations: List[BaseAnnotation] = list()

        for dataset_count, input_data in enumerate(self.mot_input_data):

            mot_class_mapper = MOTAnnotationParser.create_mot_mapper(
                mot_format=input_data.mot_format
            )

            with open(
                file=input_data.annotation_path, mode="r", encoding="'utf-8"
            ) as annotation_file:
                annotation_lines = annotation_file.readlines()

            # frame-id: annotation line
            annotation_line_dict: Dict[int, List[str]] = {}
            for annotation_line in annotation_lines:
                frame_id = int(annotation_line.split(",")[0])

                if frame_id not in annotation_line_dict:
                    annotation_line_dict[frame_id] = []

                annotation_line_dict[frame_id].append(annotation_line.strip())

            image_paths = get_file_list(
                input_dir=input_data.image_dir,
                search_subfolders=False,
                file_extension=input_data.image_format,
            )

            image_paths.sort()
            for image_id, image_path in enumerate(image_paths):

                image = cv2.imread(image_path)
                image_shape = image.shape

                replacement_string = AnnotationParser.csv_directory_replacement_string.format(
                    dataset_count
                )

                mot_builder = MOTAnnotationBuilder(
                    image_shape=image_shape,
                    image_id=image_id + 1,  # image ids are 1-based
                    annotation_line_dict=annotation_line_dict,
                    mapper=self.mapper,
                    mot_class_mapper=mot_class_mapper,
                    mot_format=input_data.mot_format,
                    ground_truth=input_data.ground_truth,
                )

                try:
                    annotation = mot_builder.build(
                        image_path=image_path,
                        annotation_path=input_data.annotation_path,
                        image_dir=input_data.image_dir,
                        annotation_dir=os.path.dirname(input_data.annotation_path),
                        replacement_string=replacement_string,
                    )

                    annotations.append(annotation)

                except ValueError as error:
                    logger.warning(
                        "%s, annotation from path %s will be skipped",
                        str(error),
                        input_data.annotation_path,
                    )
                    continue

        return annotations

    @staticmethod
    def create_mot__2015_class_mapping() -> ClassMappingConfig:
        # REMARK:
        # - The class-ids in the MOT Challenge start a 1, therefore we
        #   add an extra class in order to fulfill our definition of a class-mapping
        # - Due to related package an "Unexpected keyword argument" is raised. For now
        #   this error is ignored, but it will be fixed in future versions of related
        # - No line break are definitely more readable here

        # pylint: disable=unexpected-keyword-arg, line-too-long
        return ClassMappingConfig(
            mapping=[],
            model_classes=[
                ClassMappingModelClassesConfig(class_name="other", class_id=0),  # type: ignore[call-arg]
                ClassMappingModelClassesConfig(class_name="pedestrian", class_id=1),  # type: ignore[call-arg]
            ],
            number_model_classes=2,
        )
        # pylint: enable=unexpected-keyword-arg, line-too-long

    @staticmethod
    def create_mot__201617_class_mapping() -> ClassMappingConfig:
        # REMARK:
        # - The class-ids in the MOT Challenge start a 1, therefore we
        #   add an extra class in order to fulfill our definition of a class-mapping
        # - Due to related package an "Unexpected keyword argument" is raised. For now
        #   this error is ignored, but it will be fixed in future versions of related
        # - No line break are definitely more readable here

        mot_2015_class_mapping = MOTAnnotationParser.create_mot__2015_class_mapping()

        # pylint: disable=unexpected-keyword-arg, line-too-long
        model_classes = [
            ClassMappingModelClassesConfig(class_name="persononvehicle", class_id=2),  # type: ignore[call-arg]
            ClassMappingModelClassesConfig(class_name="car", class_id=3),  # type: ignore[call-arg]
            ClassMappingModelClassesConfig(class_name="bicycle", class_id=4),  # type: ignore[call-arg]
            ClassMappingModelClassesConfig(class_name="motorbike", class_id=5),  # type: ignore[call-arg]
            ClassMappingModelClassesConfig(class_name="nonmotorvehicle", class_id=6),  # type: ignore[call-arg]
            ClassMappingModelClassesConfig(class_name="staticperson", class_id=7),  # type: ignore[call-arg]
            ClassMappingModelClassesConfig(class_name="distractor", class_id=8),  # type: ignore[call-arg]
            ClassMappingModelClassesConfig(class_name="occluder", class_id=9),  # type: ignore[call-arg]
            ClassMappingModelClassesConfig(class_name="occluderonground", class_id=10),  # type: ignore[call-arg]
            ClassMappingModelClassesConfig(class_name="occluderfull", class_id=11),  # type: ignore[call-arg]
            ClassMappingModelClassesConfig(class_name="reflection", class_id=12),  # type: ignore[call-arg]
        ]

        model_classes.extend(mot_2015_class_mapping.model_classes)

        return ClassMappingConfig(  # type: ignore[call-arg]
            mapping=[],
            model_classes=model_classes,
            number_model_classes=len(model_classes),
        )
        # pylint: enable=unexpected-keyword-arg, line-too-long

    @staticmethod
    def create_mot__2020_class_mapping() -> ClassMappingConfig:
        """
        Creates a class mapping that

        Returns:

        """

        # REMARK:
        # - The class-ids in the MOT Challenge start a 1, therefore we
        #   add an extra class in order to fulfill our definition of a class-mapping
        # - Due to related package an "Unexpected keyword argument" is raised. For now
        #   this error is ignored, but it will be fixed in future versions of related
        # - No line break are definitely more readable here

        mot_201617_class_mapping = MOTAnnotationParser.create_mot__201617_class_mapping()

        # pylint: disable=unexpected-keyword-arg, line-too-long
        model_classes = [
            ClassMappingModelClassesConfig(class_name="crowd", class_id=13),  # type: ignore[call-arg]
        ]

        model_classes.extend(mot_201617_class_mapping.model_classes)

        return ClassMappingConfig(  # type: ignore[call-arg]
            mapping=[],
            model_classes=model_classes,
            number_model_classes=len(model_classes),
        )
        # pylint: enable=unexpected-keyword-arg, line-too-long
