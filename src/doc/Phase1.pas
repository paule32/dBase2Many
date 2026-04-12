var JsonText   : string;
var Root       : Variant;
var Proj       : Variant;
var Topics     : Variant;
var Conds      : Variant;
var TopicItem  : Variant;

var ProjectId  : string;
var RootTopic  : string;
var TopicId    : string;
var BuildId    : string;

var SL         : TStringList;
var I          : Integer;

function LoadTextFile(const FileName: string): string;
var T: TStringList;
begin
    T := TStringList.Create;
    try
        T.LoadFromFile(FileName);
        Result := T.Text;
    finally
        T.Free;
    end;
end;

function VStr(const V: Variant; Def: string = ''): string;
begin
  try
    Result := Trim(string(V));
    if Result = '' then
      Result := Def;
  except
    Result := Def;
  end;
end;

function VInt(const V: Variant; Def: Integer = 0): Integer;
begin
  try
    Result := Integer(V);
  except
    Result := Def;
  end;
end;

procedure BuildProjectFromJson(const JsonFileName: string);
begin
  var JsonText := LoadTextFile(JsonFileName);
  var Root := JSON.Parse(JsonText);
  var Proj := Root.project;
  var Conds := Root.conditions;
  var Topics := Root.topics;

  var ProjectFile := VStr(Proj.file, '');
  var ProjectTitle := VStr(Proj.title, 'Help Project');
  var ProjectAuthor := VStr(Proj.author, '');
  var ProjectVersion := VStr(Proj.version, '1.0');
  var ProjectLang := VInt(Proj.languageLcid, 1031);

  var ProjectId := '';
  if FileExists(ProjectFile) then
    ProjectId := HndProjects.OpenProject(ProjectFile, True)
  else
    ProjectId := HndProjects.NewProject(ProjectFile);

  HndProjects.SetProjectTitle(ProjectTitle);
  HndProjects.SetProjectAuthor(ProjectAuthor);
  HndProjects.SetProjectVersion(ProjectVersion);
  HndProjects.SetProjectLanguage(ProjectLang);

  HndBuilds.DeleteAllBuilds;
  var BuildId := HndBuilds.CreateBuild;
  HndBuilds.SetBuildName(BuildId, VStr(Proj.chmBuildName, 'CHM'));
  HndBuilds.SetBuildKind(BuildId, 'chm');
  HndBuilds.SetBuildEnabled(BuildId, True);
  HndBuilds.SetBuildOutput(BuildId, VStr(Proj.chmOutput, ''));

  HndTopics.DeleteAllTopics;
  var RootTopic := HndTopics.GetProjectTopic;

  for var I := 0 to Topics.length - 1 do
  begin
    var TopicItem := Topics[I];
    var TopicId := HndTopics.CreateTopic;
    HndTopics.MoveTopic(TopicId, RootTopic, htamAddChild);

    HndTopics.SetTopicCaption(
      TopicId,
      VStr(TopicItem.caption, VStr(TopicItem.helpId, 'Untitled'))
    );
    HndTopics.SetTopicHelpId(TopicId, VStr(TopicItem.helpId, ''));
    HndTopics.SetTopicHelpContext(TopicId, VInt(TopicItem.helpContext, 0));

    HndTopicsProperties.SetTopicCustomPropertyValue(TopicId, 'Html_de_dark',  VStr(TopicItem.html_de_dark, ''));
    HndTopicsProperties.SetTopicCustomPropertyValue(TopicId, 'Html_de_light', VStr(TopicItem.html_de_light, ''));
    HndTopicsProperties.SetTopicCustomPropertyValue(TopicId, 'Html_en_dark',  VStr(TopicItem.html_en_dark, ''));
    HndTopicsProperties.SetTopicCustomPropertyValue(TopicId, 'Html_en_light', VStr(TopicItem.html_en_light, ''));
    HndTopicsProperties.SetTopicCustomPropertyValue(TopicId, 'WidgetClass',   VStr(TopicItem.widgetClass, ''));
    HndTopicsProperties.SetTopicCustomPropertyValue(TopicId, 'Category',      VStr(TopicItem.category, ''));
  end;

  HndProjects.SaveProject;
end;

begin
  BuildProjectFromJson('T:\GitHub\dBase2Many\src\doc\HelpDoc.json');
end.