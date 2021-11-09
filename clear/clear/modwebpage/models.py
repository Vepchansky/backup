from django.db import models
from django.utils.html import strip_tags
from django.utils.safestring import mark_safe
from wagtail.core import blocks
from coderedcms.blocks import (
    CONTENT_STREAMBLOCKS,
    LAYOUT_STREAMBLOCKS,
    STREAMFORM_BLOCKS,
    HTML_STREAMBLOCKS,
    ContentWallBlock,
    OpenHoursBlock,
    StructuredDataActionBlock,
)
from coderedcms.models.page_models import CoderedPage
from django.utils.translation import gettext_lazy as _
from wagtail.admin.edit_handlers import (
    HelpPanel,
    FieldPanel,
    FieldRowPanel,
    InlinePanel,
    MultiFieldPanel,
    ObjectList,
    PageChooserPanel,
    StreamFieldPanel,
    TabbedInterface
)
from wagtail.core.fields import StreamField
from wagtail.search import index
from .blocks import (NewModalBlock, Answer, CardBlockScroll,
                     TestCardBlockScroll, ReusableContentBlockMode)

from wagtail.snippets.models import register_snippet

from coderedcms.blocks.content_blocks import (  # noqa
    CardBlock)

from coderedcms.blocks.layout_blocks import (
    CardGridBlock,
    GridBlock,
    HeroBlock
)

from wagtail_webstories.blocks import StoryEmbedBlock
from wagtail_webstories.models import BaseWebStoryPage
from wagtail.images.blocks import ImageChooserBlock

# Ниже переопределяются наборы блоков для StreamField WebPage

CONTENT_STREAMBLOCKS = CONTENT_STREAMBLOCKS + [
    ('newmodal', NewModalBlock(HTML_STREAMBLOCKS)),
    ('answer', Answer()),
    ('horizscroll', CardBlockScroll()),
    ('reusablemode', ReusableContentBlockMode()),
    ('story_embed', StoryEmbedBlock()),
]


LAYOUT_STREAMBLOCKS = [
    ('hero', HeroBlock([
        ('row', GridBlock(CONTENT_STREAMBLOCKS)),
        ('cardgrid', CardGridBlock([
            ('card', CardBlock()),
        ])),
        ('html', blocks.RawHTMLBlock(icon='code', form_classname='monospace', label=_('HTML'))),
    ])),
    ('row', GridBlock(CONTENT_STREAMBLOCKS)),
    ('cardgrid', CardGridBlock([
        ('card', CardBlock()),
    ])),
    ('html', blocks.RawHTMLBlock(icon='code', form_classname='monospace', label=_('HTML'))),
]

class NewCoderedWebPage(CoderedPage):
    """
    Provides a body and body-related functionality.
    This is abstract so that subclasses can override the body StreamField.
    """
    class Meta:
        verbose_name = _('CodeRed new Web Page')
        abstract = True

    template = 'coderedcms/pages/web_page.html'

    # Child pages should override based on what blocks they want in the body.
    # Default is LAYOUT_STREAMBLOCKS which is the fullest editor experience.
    body = StreamField(LAYOUT_STREAMBLOCKS, null=True, blank=True)

    # Search fields
    search_fields = (
        CoderedPage.search_fields +
        [index.SearchField('body')]
    )

    # Panels
    body_content_panels = [
        StreamFieldPanel('body'),
    ]

    @property
    def body_preview(self):
        """
        A shortened version of the body without HTML tags.
        """
        # add spaces between tags for legibility
        body = str(self.body).replace('>', '> ')
        # strip tags
        body = strip_tags(body)
        # truncate and add ellipses
        preview = body[:200] + "..." if len(body) > 200 else body
        return mark_safe(preview)

    @property
    def page_ptr(self):
        """
        Overwrite of `page_ptr` to make it compatible with wagtailimportexport.
        """
        return self.base_page_ptr

    @page_ptr.setter
    def page_ptr(self, value):
        self.base_page_ptr = value


class NewWebPage(NewCoderedWebPage):
    """
    General use page with featureful streamfield and SEO attributes.
    """
    class Meta:
        verbose_name = 'New Web Page'

    template = 'coderedcms/pages/web_page.html'

@register_snippet
class ReusableContentMode(index.Indexed, models.Model):
    """
    Snippet for resusable content in streamfields.
    """
    class Meta:
        verbose_name = _('Reusable Content Mode')
        verbose_name_plural = _('Reusable Content Mode')


    name = models.CharField(
        max_length=255,
        verbose_name=_('Name'),
    )
    content = StreamField(
        LAYOUT_STREAMBLOCKS,
        verbose_name=_('content')
    )
    search_fields = [
        index.SearchField('name', partial_match=True),
    ]

    panels = [
        FieldPanel('name'),
        StreamFieldPanel('content')
    ]

    def __str__(self):
        return self.name

class StoryPage(BaseWebStoryPage):
    
    body = StreamField([
        ('card', blocks.StructBlock([
            ('title', blocks.CharBlock()),
            ('text', blocks.TextBlock()),
            ('image', ImageChooserBlock()),
        ])
        )
    ], blank=True, null=True)

    content_panels = BaseWebStoryPage.content_panels + [
        StreamFieldPanel('body')
    ]

    template = 'modwebpage/story_page.html'
