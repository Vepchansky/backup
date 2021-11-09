from coderedcms.blocks.base_blocks import BaseBlock, BaseLayoutBlock
from coderedcms.blocks.content_blocks import CardBlock
from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.snippets.blocks import SnippetChooserBlock
from django.utils.translation import gettext_lazy as _
from coderedcms.blocks import  HTML_STREAMBLOCKS
from coderedcms.blocks.html_blocks import ButtonBlock
from wagtail_webstories.blocks import StoryEmbedBlock
from .models import CONTENT_STREAMBLOCKS

class Answer(BaseBlock):
     
     body = blocks.StreamBlock([
         ('choiseandanswer', blocks.StructBlock([
             ('choise', blocks.RichTextBlock()),
             ('answer', blocks.RichTextBlock()),
             ('HTML', blocks.RawHTMLBlock(required=False)),
         ]))
     ])

     class Meta:
         template = 'choiseblock/choiseblock.html'

     """
     A component of information with image, text, and buttons.
     """


CONTENT_STREAMBLOCKS = CONTENT_STREAMBLOCKS + [
    ('answer', Answer()),
    ('story_embed', StoryEmbedBlock()),
]

class CardScroll(BaseLayoutBlock):
    
    image = ImageChooserBlock(
        required=False,
        max_length=255,
        label=_('Image'),
    )
    title = blocks.CharBlock(
        required=False,
        max_length=255,
        label=_('Title'),
    )

    content = blocks.StreamBlock(
        [],
        label=_('Modal content'),
    )

class TestCardBlock(CardBlock):
    
    modal = blocks.StreamBlock(CONTENT_STREAMBLOCKS,
                               label=_('Modal content'))

class TestCardBlockScroll(BaseBlock):
    """
    A component of information with image, text, and buttons.
    """
    number = blocks.IntegerBlock()

    body = blocks.StreamBlock([
         ('cardscrollblock', blocks.StructBlock([
             ('card', TestCardBlock(required=False, blank=True)),
         ]))
     ])

    class Meta:
        template = 'cardblockscroll/cardblockscroll.html'

class CardBlockScroll(BaseBlock):
    """
    A component of information with image, text, and buttons.
    """
    number = blocks.IntegerBlock()

    body = blocks.StreamBlock([
         ('cardscrollblock', blocks.StructBlock([
             ('image', ImageChooserBlock(required=False, blank=True)),
             ('title', blocks.CharBlock(unicue=True, required=False)),
             ('subtitle', blocks.CharBlock(required=False)),
             ('description', blocks.RichTextBlock(
                 features=['bold', 'italic', 'ol', 'ul', 'hr', 'link', 'document-link'],
                 label=_('Body'),
                 required=False,
             )),
             ('links', blocks.StreamBlock(
                 [('Links', ButtonBlock())],
                 blank=True,
                 required=False,
                 label=_('Links'),
             )),
             ('modal', blocks.StreamBlock(CONTENT_STREAMBLOCKS,
                 label=_('Modal content'),
                 required=False,
             )),
         ]))
     ])

    class Meta:
        template = 'cardblockscroll/cardblockscroll.html'


class NewModalBlock(CardBlock, BaseLayoutBlock):
    """
    Renders a button that then opens a popup/modal with content.
    """
    header = blocks.CharBlock(
        required=False,
        max_length=255,
        label=_('Modal heading'),
    )
    content = blocks.StreamBlock(
        [],
        label=_('Modal content'),
    )

    class Meta:
        template = 'newmodblock/newmodblock.html'
        icon = 'fa-window-maximize'
        label = _('CardModal')

class ReusableContentBlockMode(BaseBlock):
    """
    Enables choosing a ResusableContent snippet.
    """
    content = SnippetChooserBlock('modwebpage.ReusableContentMode')

    class Meta:
        icon = 'fa-recycle'
        label = _('Reusable Content')
        template = 'coderedcms/blocks/reusable_content_block.html'
