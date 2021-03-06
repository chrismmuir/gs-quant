"""
Copyright 2019 Goldman Sachs.
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an
"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
KIND, either express or implied.  See the License for the
specific language governing permissions and limitations
under the License.
"""
from dataclasses import dataclass, asdict
from typing import Dict, List

from gs_quant.analytics.core.processor import BaseProcessor

DEFAULT_WIDTH = 100


class RenderType:
    DEFAULT = 'default'
    HEATMAP = 'heatmap'


@dataclass
class ColumnFormat:
    renderType: RenderType = RenderType.DEFAULT
    precision: int = 2
    humanReadable: bool = True


class DataColumn:
    """Base class for grid column"""

    def __init__(self,
                 name: str,
                 processor: BaseProcessor,
                 format: ColumnFormat = ColumnFormat(),
                 width: int = DEFAULT_WIDTH):
        """ Data row

        :param name: Name of the column
        :param processor: Processor to apply to the column for calculation
        :param format: Formatting information for the column result
        :param width: Size of the column in pixels when presented on the UI
        """
        self.name = name
        self.processor = processor
        self.format = format
        self.width = width

    def as_dict(self):
        return {
            'name': self.name,
            'processorName': self.processor.__class__.__name__,
            **self.processor.as_dict(),
            'format': asdict(self.format),
            'width': self.width
        }

    @classmethod
    def from_dict(cls, obj: Dict, reference_list: List):
        processor = BaseProcessor.from_dict(obj, reference_list)

        return DataColumn(name=obj['name'],
                          processor=processor,
                          format=ColumnFormat(**obj.get('format', {})),
                          width=obj.get('width', DEFAULT_WIDTH))
