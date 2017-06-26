# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-26 21:51
from __future__ import unicode_literals

import core.models.attachment
import core.models.base
import core.models.data_file
import core.models.experiment_attachment
import core.models.experiment_data_file
import core.models.project_attachment
from django.conf import settings
import django.core.files.storage
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('description', models.TextField()),
                ('object_id', models.PositiveIntegerField()),
                ('file', models.FileField(storage=core.models.base.UniqueFileSystemStorage(), upload_to=core.models.attachment.Attachment.get_upload_path)),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='core_attachment_creator', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'attachment',
                'ordering': ['-date_created'],
            },
        ),
        migrations.CreateModel(
            name='ContextGene',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('context', models.CharField(choices=[('All', 'All')], max_length=255)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='core_contextgene_creator', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'context_gene',
                'ordering': ['-date_created'],
            },
        ),
        migrations.CreateModel(
            name='DataFile',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('file', models.FileField(storage=django.core.files.storage.FileSystemStorage(base_url='/tmp/paperlims'), upload_to=core.models.data_file.get_datafile_upload_path)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='core_datafile_creator', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'data_file',
                'ordering': ['-date_created'],
            },
        ),
        migrations.CreateModel(
            name='Experiment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('type', models.CharField(choices=[('Other', 'Other')], max_length=255)),
                ('status', models.CharField(choices=[('new', 'new'), ('open', 'open'), ('active', 'active'), ('closed', 'closed'), ('locked', 'locked'), ('retired', 'retired'), ('deleted', 'deleted'), ('archived', 'archived'), ('replaced', 'replaced'), ('complete', 'complete')], default='active', max_length=255)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='core_experiment_creator', to=settings.AUTH_USER_MODEL)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='experiment_owner', to=settings.AUTH_USER_MODEL)),
                ('polymorphic_ctype', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_core.experiment_set+', to='contenttypes.ContentType')),
            ],
            options={
                'db_table': 'experiment',
                'ordering': ['-date_created'],
            },
        ),
        migrations.CreateModel(
            name='ExperimentAttachment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('type', models.CharField(choices=[('Word', 'Word'), ('Text', 'Text'), ('CSV', 'CSV'), ('Excel', 'Excel'), ('PDF', 'PDF'), ('Other', 'Other')], max_length=255)),
                ('file', models.FileField(upload_to=core.models.experiment_attachment.ExperimentAttachment.get_upload_path)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='core_experimentattachment_creator', to=settings.AUTH_USER_MODEL)),
                ('experiment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Experiment')),
            ],
            options={
                'db_table': 'experiment_attachment',
                'ordering': ['-date_created'],
            },
        ),
        migrations.CreateModel(
            name='ExperimentDataFile',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('file', models.FileField(storage=core.models.base.UniqueFileSystemStorage(), upload_to=core.models.experiment_data_file.ExperimentDataFile.get_upload_path)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='core_experimentdatafile_creator', to=settings.AUTH_USER_MODEL)),
                ('experiment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Experiment')),
                ('polymorphic_ctype', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_core.experimentdatafile_set+', to='contenttypes.ContentType')),
            ],
            options={
                'db_table': 'experiment_data_file',
                'ordering': ['-date_created'],
            },
        ),
        migrations.CreateModel(
            name='Gene',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('official_symbol', models.CharField(max_length=255)),
                ('official_full_name', models.CharField(max_length=255)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='core_gene_creator', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'gene',
                'ordering': ['-date_created'],
            },
        ),
        migrations.CreateModel(
            name='LabelFormat',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('format', models.TextField()),
                ('content_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='core_labelformat_creator', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'label formats',
                'db_table': 'label_format',
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='core_location_creator', to=settings.AUTH_USER_MODEL)),
                ('parent_location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Location')),
            ],
            options={
                'verbose_name_plural': 'locations',
                'db_table': 'location',
            },
        ),
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='core_material_creator', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'materials',
                'db_table': 'material',
            },
        ),
        migrations.CreateModel(
            name='MaterialLink',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='core_materiallink_creator', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'material links',
                'db_table': 'material_link',
            },
        ),
        migrations.CreateModel(
            name='MaterialToMaterial',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source_material', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='source_materials', to='core.Material')),
                ('target_material', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='target_materials', to='core.Material')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.MaterialLink')),
            ],
            options={
                'verbose_name_plural': 'material to materials',
                'db_table': 'material_to_material',
            },
        ),
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('note', models.TextField()),
                ('note_type', models.CharField(choices=[('alert', 'alert'), ('info', 'info')], max_length=255)),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='core_note_creator', to=settings.AUTH_USER_MODEL)),
                ('parent_note', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='parent', to='core.Note')),
            ],
            options={
                'db_table': 'note',
            },
        ),
        migrations.CreateModel(
            name='Organ',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='core_organ_creator', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'organ',
                'ordering': ['-date_created'],
            },
        ),
        migrations.CreateModel(
            name='Plate',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('status', models.CharField(choices=[('new', 'new'), ('open', 'open'), ('active', 'active'), ('closed', 'closed'), ('locked', 'locked'), ('retired', 'retired'), ('deleted', 'deleted'), ('archived', 'archived'), ('replaced', 'replaced'), ('complete', 'complete')], max_length=255)),
                ('type', models.CharField(choices=[('96', '96'), ('384', '384')], max_length=255)),
                ('replicate', models.CharField(max_length=255)),
                ('dimension', models.CharField(blank=True, choices=[('96', '96'), ('384', '384')], max_length=255, null=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='core_plate_creator', to=settings.AUTH_USER_MODEL)),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='plate_owner', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'plate',
                'ordering': ['-date_created'],
            },
        ),
        migrations.CreateModel(
            name='Printer',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('type', models.CharField(choices=[('barcode', 'barcode')], max_length=255)),
                ('address', models.CharField(blank=True, max_length=255, null=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='core_printer_creator', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'printers',
                'db_table': 'printer',
            },
        ),
        migrations.CreateModel(
            name='PrinterToLabelFormat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label_format', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.LabelFormat')),
                ('printer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Printer')),
            ],
            options={
                'verbose_name_plural': 'printer to label formats',
                'db_table': 'printer_to_labelformat',
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('type', models.CharField(choices=[('internal', 'internal'), ('external', 'external'), ('other', 'other')], max_length=255)),
                ('status', models.CharField(choices=[('new', 'new'), ('open', 'open'), ('active', 'active'), ('closed', 'closed'), ('locked', 'locked'), ('retired', 'retired'), ('deleted', 'deleted'), ('archived', 'archived'), ('replaced', 'replaced'), ('complete', 'complete')], default='active', max_length=255)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='core_project_creator', to=settings.AUTH_USER_MODEL)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_owner', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'project',
            },
        ),
        migrations.CreateModel(
            name='ProjectAttachment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('type', models.CharField(choices=[('Word', 'Word'), ('Text', 'Text'), ('CSV', 'CSV'), ('Excel', 'Excel'), ('PDF', 'PDF'), ('Other', 'Other')], max_length=255)),
                ('file', models.FileField(upload_to=core.models.project_attachment.ProjectAttachment.get_upload_path)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='core_projectattachment_creator', to=settings.AUTH_USER_MODEL)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Project')),
            ],
            options={
                'db_table': 'project_attachment',
            },
        ),
        migrations.CreateModel(
            name='RecordNote',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('table_name', models.CharField(max_length=255)),
                ('record_id', models.CharField(max_length=255)),
                ('note', models.TextField()),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='core_recordnote_creator', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'record_note',
            },
        ),
        migrations.CreateModel(
            name='Sample',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('name', core.models.base.CaseInsensitiveCharField(blank=True, max_length=255, null=True, unique=True)),
                ('description', models.TextField(blank=True)),
                ('status', models.CharField(choices=[('new', 'new'), ('open', 'open'), ('active', 'active'), ('closed', 'closed'), ('locked', 'locked'), ('retired', 'retired'), ('deleted', 'deleted'), ('archived', 'archived'), ('replaced', 'replaced'), ('complete', 'complete')], default='active', max_length=255)),
                ('lot', models.CharField(blank=True, max_length=255, null=True)),
                ('volume', models.CharField(blank=True, max_length=255, null=True)),
                ('concentration', models.CharField(blank=True, max_length=255, null=True)),
                ('concentration_units', models.CharField(blank=True, max_length=255, null=True)),
                ('unit_count', models.CharField(blank=True, max_length=255, null=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='core_sample_creator', to=settings.AUTH_USER_MODEL)),
                ('material', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Material')),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('polymorphic_ctype', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_core.sample_set+', to='contenttypes.ContentType')),
                ('project', models.ManyToManyField(blank=True, to='core.Project')),
            ],
            options={
                'verbose_name_plural': 'samples',
                'db_table': 'sample',
                'ordering': ['-date_created'],
            },
        ),
        migrations.CreateModel(
            name='SampleBucket',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='core_samplebucket_creator', to=settings.AUTH_USER_MODEL)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('projects', models.ManyToManyField(blank=True, to='core.Project')),
                ('samples', models.ManyToManyField(blank=True, to='core.Sample')),
            ],
            options={
                'verbose_name_plural': 'sample buckets',
                'db_table': 'sample_bucket',
            },
        ),
        migrations.CreateModel(
            name='SampleLink',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='core_samplelink_creator', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'sample links',
                'db_table': 'sample_link',
            },
        ),
        migrations.CreateModel(
            name='SampleToSample',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source_sample', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='source_samples', to='core.Sample')),
                ('target_sample', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='target_samples', to='core.Sample')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.SampleLink')),
            ],
            options={
                'verbose_name_plural': 'sample to samples',
                'db_table': 'sample_to_sample',
            },
        ),
        migrations.CreateModel(
            name='SampleType',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='core_sampletype_creator', to=settings.AUTH_USER_MODEL)),
                ('source_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.SampleType')),
            ],
            options={
                'verbose_name_plural': 'sample types',
                'db_table': 'sample_type',
            },
        ),
        migrations.CreateModel(
            name='SampleUse',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('action', models.TextField()),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='core_sampleuse_creator', to=settings.AUTH_USER_MODEL)),
                ('project', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Project')),
                ('sample', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Sample')),
            ],
            options={
                'verbose_name_plural': 'sample use',
                'db_table': 'sample_use',
            },
        ),
        migrations.CreateModel(
            name='SiteMessage',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('message', models.TextField()),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='core_sitemessage_creator', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'site_message',
            },
        ),
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='core_source_creator', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'sources',
                'db_table': 'source',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Storage',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('status', models.CharField(choices=[('new', 'new'), ('open', 'open'), ('active', 'active'), ('closed', 'closed'), ('locked', 'locked'), ('retired', 'retired'), ('deleted', 'deleted'), ('archived', 'archived'), ('replaced', 'replaced'), ('complete', 'complete')], max_length=255)),
                ('location', models.CharField(blank=True, max_length=255, null=True)),
                ('holds_containers', models.BooleanField()),
                ('holds_samples', models.BooleanField()),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='core_storage_creator', to=settings.AUTH_USER_MODEL)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Storage')),
            ],
            options={
                'verbose_name_plural': 'storage',
                'db_table': 'storage',
            },
        ),
        migrations.CreateModel(
            name='StorageType',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='core_storagetype_creator', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'storage types',
                'db_table': 'storage_type',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('name', core.models.base.CaseInsensitiveCharField(max_length=255, unique=True)),
                ('description', models.TextField(blank=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='core_tag_creator', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'tag',
                'ordering': ['-date_created'],
            },
        ),
        migrations.CreateModel(
            name='Well',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('index', models.IntegerField()),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='core_well_creator', to=settings.AUTH_USER_MODEL)),
                ('plate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Plate')),
                ('polymorphic_ctype', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_core.well_set+', to='contenttypes.ContentType')),
            ],
            options={
                'db_table': 'well',
                'ordering': ['-date_created'],
            },
        ),
        migrations.CreateModel(
            name='WellContent',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('amount_value', models.CharField(blank=True, max_length=255, null=True)),
                ('amount_unit', models.CharField(blank=True, max_length=255, null=True)),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='core_wellcontent_creator', to=settings.AUTH_USER_MODEL)),
                ('well', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Well')),
            ],
            options={
                'db_table': 'well_content',
            },
        ),
        migrations.CreateModel(
            name='WellLink',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='core_welllink_creator', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'well links',
                'db_table': 'well_link',
            },
        ),
        migrations.CreateModel(
            name='WellToWell',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source_sample', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='source_wells', to='core.Well')),
                ('target_sample', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='target_wells', to='core.Well')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.WellLink')),
            ],
            options={
                'verbose_name_plural': 'wells to wells',
                'db_table': 'well_to_well',
            },
        ),
        migrations.AddField(
            model_name='well',
            name='well_links',
            field=models.ManyToManyField(blank=True, related_name='linked_to', through='core.WellToWell', to='core.Well'),
        ),
        migrations.AddField(
            model_name='storage',
            name='type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.StorageType'),
        ),
        migrations.AddField(
            model_name='sample',
            name='sample_links',
            field=models.ManyToManyField(blank=True, related_name='linked_to', through='core.SampleToSample', to='core.Sample'),
        ),
        migrations.AddField(
            model_name='sample',
            name='sample_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.SampleType'),
        ),
        migrations.AddField(
            model_name='sample',
            name='source',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Source'),
        ),
        migrations.AddField(
            model_name='sample',
            name='storage',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Storage'),
        ),
        migrations.AddField(
            model_name='printer',
            name='label_formats',
            field=models.ManyToManyField(blank=True, through='core.PrinterToLabelFormat', to='core.LabelFormat'),
        ),
        migrations.AddField(
            model_name='printer',
            name='location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Location'),
        ),
        migrations.AddField(
            model_name='material',
            name='material_links',
            field=models.ManyToManyField(blank=True, related_name='linked_to', through='core.MaterialToMaterial', to='core.Material'),
        ),
        migrations.AddField(
            model_name='material',
            name='polymorphic_ctype',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_core.material_set+', to='contenttypes.ContentType'),
        ),
        migrations.AddField(
            model_name='experiment',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Project'),
        ),
        migrations.AddField(
            model_name='datafile',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Project'),
        ),
        migrations.AddField(
            model_name='contextgene',
            name='gene',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Gene'),
        ),
        migrations.AlterUniqueTogether(
            name='well',
            unique_together=set([('name', 'plate')]),
        ),
        migrations.AlterUniqueTogether(
            name='tag',
            unique_together=set([('name',)]),
        ),
        migrations.AlterUniqueTogether(
            name='storage',
            unique_together=set([('name',)]),
        ),
        migrations.AlterUniqueTogether(
            name='sample',
            unique_together=set([('name',)]),
        ),
        migrations.AlterUniqueTogether(
            name='plate',
            unique_together=set([('name', 'replicate')]),
        ),
        migrations.AlterUniqueTogether(
            name='material',
            unique_together=set([('name',)]),
        ),
        migrations.AlterUniqueTogether(
            name='gene',
            unique_together=set([('name',)]),
        ),
        migrations.AlterUniqueTogether(
            name='experiment',
            unique_together=set([('name', 'project')]),
        ),
        migrations.AlterUniqueTogether(
            name='contextgene',
            unique_together=set([('gene', 'context')]),
        ),
    ]
